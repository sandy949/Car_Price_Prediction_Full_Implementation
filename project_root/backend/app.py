import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np
import pandas as pd
import csv
import json
import joblib
from flask import Flask, request, jsonify, render_template, Blueprint
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from io import TextIOWrapper
from backend.redis_client import redis_client
from sqlalchemy import cast, Date
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.auth.jwt_utils import get_current_user

from sqlalchemy.orm import joinedload
from utils import utils
from config import config
from data_transformation import data_transformation
from models import model
from backend.db_models import Base, User, TaskManager, TaskLogger, RoleEnum  # import your models
from backend.extensions import limiter



# --- DB Setup ---
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost/car_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# --- Flask App ---
app = Flask(__name__, template_folder="templates")

from backend.routes.task_routes import task_bp, routes  # <- import both task_bp and routes

# Register blueprints
app.register_blueprint(task_bp)
app.register_blueprint(routes)
limiter.init_app(app)
# -------------------- UI ROUTES -------------------- #
@app.route('/')
def home():
    """Renders the main form for car price prediction."""
    return render_template('form.html')


@app.route('/predict', methods=['POST'])
def predict():
    """Processes user input and returns predicted car price."""
    try:
        if request.is_json:
            input_data = request.json
        else:
            input_data = request.form.to_dict()

        print("Input received:", input_data)
        X = data_transformation.process_input(input_data)
        prediction = model.predict(X, config.MODEL)
        return render_template('result.html', price=float(prediction[0]))
    except Exception as e:
        print("Prediction error:", str(e))
        return jsonify({'error': str(e)}), 500


# -------------------- TASK ROUTES -------------------- #

@app.errorhandler(429)
def ratelimit_handler(e):
    """Handles rate limit errors and returns a JSON response."""
    return jsonify({
        "error": "rate_limit_exceeded",
        "message": "Too many requests. Please try again later."
    }), 429
    
@app.route("/task/<int:task_logger_id>", methods=["GET"])
@limiter.limit("20/minute")
def get_task_details(task_logger_id):
    """Returns task and audit log details for the given logger ID."""
    db = SessionLocal()
    try:
        log = db.query(TaskLogger)\
            .options(joinedload(TaskLogger.task))\
            .filter(TaskLogger.id == task_logger_id)\
            .first()
        
        if not log:
            return jsonify({"error": "Task log not found"}), 404

        return jsonify({
            "task_log_id": log.id,
            "task_id": log.task_id,
            "old_status": log.old_status,
            "new_status": log.new_status,
            "changed_by": log.changed_by,
            "changed_at": log.changed_at.isoformat(),
            "task": {
                "title": log.task.title,
                "description": log.task.description,
                "status": log.task.status
            }
        })

    finally:
        db.close()

task_bp = Blueprint("task_routes", __name__)

@task_bp.route('/tasks', methods=['GET'])
@limiter.limit("60/minute")
def get_tasks_by_date():
    """Returns audit logs for a specific date using Redis cache."""
    date_param = request.args.get("date")
    if not date_param:
        return jsonify({"error": "Missing date parameter"}), 400
    
    try:
        # Parse date string
        date = datetime.strptime(date_param, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    cache_key = f"tasks:{date.isoformat()}"
    
    # Try Redis cache
    cached = redis_client.get(cache_key)
    if cached:
        return jsonify({"source": "cache", "results": json.loads(cached)})

    # Query DB
    session = SessionLocal()
    tasks = session.query(TaskLogger).filter(cast(TaskLogger.timestamp, Date) == date).all()

    result = [{
        "id": t.id,
        "task_id": t.task_id,
        "old_status": t.old_status,
        "new_status": t.new_status,
        "changed_by": t.changed_by,
        "timestamp": t.timestamp.isoformat()
    } for t in tasks]

    # Store in Redis (TTL: 3600 seconds = 1 hour)
    redis_client.setex(cache_key, 3600, json.dumps(result))
    
    return jsonify({"source": "db", "results": result})

@app.route('/tasks', methods=['GET'])
@limiter.limit("30/minute")
def get_logged_tasks():
    """Returns paginated list of task audit logs."""
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        offset = (page - 1) * limit

        session = SessionLocal()
        query = session.query(TaskLogger).options(joinedload(TaskLogger.task)).offset(offset).limit(limit)
        logs = query.all()

        results = []
        for log in logs:
            results.append({
                "id": log.id,
                "task_id": log.task_id,
                "old_status": log.old_status,
                "new_status": log.new_status,
                "changed_by": log.changed_by,
                "changed_at": log.changed_at.isoformat() if log.changed_at else None
            })

        return jsonify({
            "page": page,
            "limit": limit,
            "results": results
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/upload-csv', methods=['POST'])
@limiter.limit("5/minute")
def upload_csv():
    """Handles uploading a CSV file and inserting tasks into the DB."""
    if 'file' not in request.files:
        return jsonify({"error": "No file part in request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Optional: validate file type
    if not file.filename.endswith('.csv'):
        return jsonify({"error": "Invalid file type"}), 400

    session = SessionLocal()

    try:
        stream = TextIOWrapper(file.stream, encoding='utf-8')
        reader = csv.DictReader(stream)

        for row in reader:
            task = TaskManager(
                title=row.get("title"),
                description=row.get("description"),
                status=row.get("status", "pending")
            )
            session.add(task)

        session.commit()
        return jsonify({"message": "CSV uploaded successfully"}), 201

    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        session.close()

@app.route('/task/<int:task_id>/update', methods=['POST'])
@app.route('/task/<int:task_id>', methods=['PUT'])
@limiter.limit("10/minute")
@jwt_required()
def update_task(task_id):
    """
    Updates a task's status.
    Logs the change in TaskLogger with user attribution.
    Applies RBAC based on user role and ownership.
    """
    session = SessionLocal()
    try:
        data = request.get_json()
        new_status = data.get("status")
        if not new_status:
            return jsonify({"error": "Missing new status"}), 400

        current_user = get_current_user()
        if not current_user:
            return jsonify({"error": "Unauthorized"}), 401

        task = session.query(TaskManager).filter_by(id=task_id).first()
        if not task:
            return jsonify({"error": "Task not found"}), 404

        # --- RBAC enforcement ---
        if current_user.role not in [RoleEnum.admin, RoleEnum.manager] and task.user_id != current_user.id:
            return jsonify({"error": "Access denied"}), 403

        old_status = task.status
        task.status = new_status

        # --- Audit log ---
        log = TaskLogger(
            task=task,
            old_status=old_status,
            new_status=new_status,
            changed_by=current_user.username
        )
        session.add(log)
        session.commit()
        return jsonify({"message": "Task updated successfully"})

    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        session.close()


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
