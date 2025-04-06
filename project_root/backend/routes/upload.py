# backend/routes/upload.py
import pandas as pd
from flask import Blueprint, request, jsonify
from backend.schemas.task_schemas import TaskCSVSchema
from backend.db import SessionLocal
from backend.db_models import TaskManager, User

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload-csv', methods=['POST'])
def upload_csv():
    """
    Upload and bulk insert tasks from a CSV file.

    Expects a CSV file with `title` and `description` fields.
    Validates each row using Pydantic schema and inserts into the database.
    
    Returns:
        JSON response with count of inserted tasks and list of failed rows.
    """
    session = SessionLocal()

    if 'file' not in request.files:
        return jsonify({'error': 'CSV file not provided'}), 400

    file = request.files['file']
    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'Invalid file format'}), 400

    df = pd.read_csv(file)
    success = 0
    errors = []

    for idx, row in df.iterrows():
        try:
            task_data = TaskCSVSchema(**row.to_dict())
            task = TaskManager(
                title=task_data.title,
                description=task_data.description,
                user_id=1  # TEMP: Assuming admin/manager exists with id=1
            )
            session.add(task)
            success += 1
        except Exception as e:
            errors.append({'row': idx, 'error': str(e)})

    session.commit()
    session.close()

    return jsonify({'inserted': success, 'errors': errors})
