from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, Text, DateTime, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

Base = declarative_base()

class Car(Base):
    """
    Table: cars
    Stores raw vehicle data for predictions and analytics.
    """
    __tablename__ = 'cars'

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    manufacturer = Column(String, nullable=False)
    model = Column(String, nullable=False)
    condition = Column(String)
    cylinders = Column(String)
    fuel = Column(String)
    odometer = Column(Float)
    transmission = Column(String)
    drive = Column(String)
    size = Column(String)
    type = Column(String)
    paint_color = Column(String)

# --- Role Enum ---
class RoleEnum(str, enum.Enum):
    """
    Enum for user roles used in role-based access control (RBAC).
    """
    admin = "admin"
    manager = "manager"
    user = "user"

# --- User model ---
class User(Base):
    """
    Table: users
    Represents a registered user with a username and role.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False, index=True)
    role = Column(Enum(RoleEnum), nullable=False, default=RoleEnum.user)

    tasks = relationship("TaskManager", back_populates="creator", lazy="dynamic", cascade="all, delete-orphan")


# --- TaskManager model ---
class TaskManager(Base):
    """
    Table: tasks
    Main table for user-created tasks. Each task is linked to a creator and can have multiple logs.
    """
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(String, default="pending", index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    creator = relationship("User", back_populates="tasks", lazy="joined")

    logs = relationship("TaskLogger", back_populates="task", lazy="select", cascade="all, delete-orphan")


# --- TaskLogger model ---
class TaskLogger(Base):
    """
    Table: task_logs
    Audit log table that records status changes for tasks.
    Includes who made the change and when.
    """
    __tablename__ = 'task_logs'

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey('tasks.id', ondelete="CASCADE"))
    old_status = Column(String)
    new_status = Column(String)
    changed_by = Column(String)
    changed_at = Column(DateTime(timezone=True), server_default=func.now())

    task = relationship("TaskManager", back_populates="logs")