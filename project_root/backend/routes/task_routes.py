# backend/routes/task_routes.py

from flask import Blueprint, request, jsonify, g
from backend.db_models import TaskManager, TaskLogger, User
from backend.rbac import is_authorized
from sqlalchemy.orm import Session
from backend.db import SessionLocal  
from backend.schemas.task_schemas import TaskCreateSchema
from backend.auth.jwt_utils import token_required
from flask_jwt_extended import jwt_required
from backend.auth.jwt_utils import get_current_user
import pydantic
# from backend.schemas.task_schemas import TaskUpdateSchema


routes = Blueprint('routes', __name__)

# TEMP: simulate a logged-in user
def get_current_user():
    return SessionLocal.session.query(User).filter_by(username="admin").first()

task_bp = Blueprint('task_bp', __name__,url_prefix="/api")

@task_bp.route("/task/<int:task_id>", methods=["PUT"])
@token_required
def update_task(task_id):
    """
    Update an existing task's title, description, or status.
    Only the task creator or an admin can perform this operation.

    Args:
        task_id (int): ID of the task to update.

    Returns:
        JSON response with success message or error.
    """
    user = g.current_user  # 🟢 access user here
    session = SessionLocal()

    task = session.query(TaskManager).filter_by(id=task_id).first()
    if not task:
        return jsonify({"error": "Task not found"}), 404

    # Only allow creator or admin to edit
    if task.user_id != user.id and user.role != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    task.status = data.get("status", task.status)
    session.commit()

    return jsonify({"message": "Task updated successfully"}), 200




@task_bp.route("/task", methods=["POST"])
@token_required
def create_task(current_user_id):
    """
    Create a new task with validated input using Pydantic schema.

    Args:
        current_user_id (int): ID of the authenticated user.

    Returns:
        JSON response containing task details or validation errors.
    """
    try:
        data = request.get_json()
        task_data = TaskCreateSchema(**data)
    except pydantic.ValidationError as e:
        return jsonify({"errors": e.errors()}), 400

    task = TaskManager(
        title=task_data.title,
        description=task_data.description,
        status=task_data.status,
        user_id=current_user_id
    )

    SessionLocal.session.add(task)
    SessionLocal.session.commit()

    return jsonify({
        "message": "Task created",
        "task": {
            "id": task.id,
            "title": task.title,
            "status": task.status,
            "description": task.description
        }
    }), 201

