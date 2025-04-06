from pydantic import BaseModel, Field
from typing import Optional, Literal

class TaskCSVSchema(BaseModel):
    """
    Schema for tasks imported via CSV upload.

    Fields:
        title (str): Title of the task (required).
        description (Optional[str]): Optional description of the task.
    """
    title: str
    description: Optional[str] = None


class TaskCreateSchema(BaseModel):
    """
    Schema for validating new task creation via API.

    Fields:
        title (str): Title of the task, must be at least 3 characters.
        description (str): Description of the task, minimum 5 characters.
        status (str): Must be one of 'pending', 'in_progress', or 'completed'.
    """
    title: str = Field(..., min_length=3)
    description: str = Field(..., min_length=5)
    status: Literal["pending", "in_progress", "completed"]