
from sqlalchemy.orm import Session

from app.models import db_models
from app.models.user import TaskCreate, TaskUpdate


# CREATE TASK
def create_task(db: Session, task_data: TaskCreate):
    user = db.query(db_models.User).filter(
        db_models.User.id == task_data.user_id
    ).first()

    if user is None:
        return None

    new_task = db_models.Task(
        title=task_data.title,
        description=task_data.description,
        status=task_data.status,
        user_id=task_data.user_id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


# GET ALL TASKS
def get_all_tasks(db: Session, task_status=None):
    query = db.query(db_models.Task)

    if task_status is not None:
        query = query.filter(
            db_models.Task.status == task_status
        )

    return query.all()


# GET TASK BY ID
def get_task_by_id(db: Session, task_id: int):
    return db.query(db_models.Task).filter(
        db_models.Task.id == task_id
    ).first()


# UPDATE TASK
def update_task(db: Session, task_id: int, task_data: TaskUpdate):
    task = get_task_by_id(db, task_id)

    if task is None:
        return None

    update_data = task_data.model_dump(exclude_unset=True)

    # Validate assigned user
    if "user_id" in update_data:
        if update_data["user_id"] is None:
            return None

        user = db.query(db_models.User).filter(
            db_models.User.id == update_data["user_id"]
        ).first()

        if user is None:
            return None

    # Prevent empty values in required fields
    for field in ("title", "status"):
        if field in update_data and update_data[field] is None:
            return None

    # Update task fields, including work_notes
    for key, value in update_data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    return task


# DELETE TASK
def delete_task(db: Session, task_id: int):
    task = get_task_by_id(db, task_id)

    if task is None:
        return False

    db.delete(task)
    db.commit()

    return True