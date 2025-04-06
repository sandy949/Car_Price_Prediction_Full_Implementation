from db import SessionLocal
from db_models import User, TaskManager

def seed_data():
    """
    Seed the database with sample users and a task.

    This function performs the following steps:
    1. Creates three users with roles: admin, manager, and user.
    2. Commits the users to the database.
    3. Creates one task titled "Fix Bug" and assigns it to the manager.
    4. Commits the task to the database.
    """
    session = SessionLocal()

    # Create users
    admin = User(username="admin_user", role="admin")
    manager = User(username="manager_user", role="manager")
    regular = User(username="regular_user", role="user")

    session.add_all([admin, manager, regular])
    session.commit()

    # Assign a task to the manager
    task = TaskManager(title="Fix Bug", description="Fix issue #231", creator=manager)
    session.add(task)
    session.commit()

    print("Database seeded with sample users and task.")
    session.close()

if __name__ == "__main__":
    seed_data()
