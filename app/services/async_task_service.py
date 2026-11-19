
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import db_models
from app.models.user import TaskCreate, TaskUpdate


# CREATE TASK
async def create_task(db: AsyncSession, task_data: TaskCreate):
    result = await db.execute(
        select(db_models.User).where(
            db_models.User.id == task_data.user_id
        )
    )
    user = result.scalar_one_or_none()

    if user is None:
        return None

    new_task = db_models.Task(
        title=task_data.title,
        description=task_data.description,
        status=task_data.status,
        user_id=task_data.user_id
    )

    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)

    return new_task


# GET ALL TASKS WITH PAGINATION, SEARCH AND FILTERS
async def get_all_tasks(
    db: AsyncSession,
    task_status=None,
    user_id=None,
    page: int = 1,
    limit: int = 10,
    search=None,
    assigned_user_id=None
):
    query = select(db_models.Task)

    if task_status is not None:
        query = query.where(
            db_models.Task.status == task_status
        )

    if user_id is not None:
        query = query.where(
            db_models.Task.user_id == user_id
        )

    if assigned_user_id is not None:
        query = query.where(
            db_models.Task.user_id == assigned_user_id
        )

    if search:
        query = query.where(
            db_models.Task.title.ilike(f"%{search}%")
        )

    offset = (page - 1) * limit

    query = query.order_by(
        db_models.Task.id
    ).offset(offset).limit(limit)

    result = await db.execute(query)

    return result.scalars().all()


# GET TASK BY ID
async def get_task_by_id(
    db: AsyncSession,
    task_id: int
):
    result = await db.execute(
        select(db_models.Task).where(
            db_models.Task.id == task_id
        )
    )

    return result.scalar_one_or_none()


# UPDATE TASK
async def update_task(
    db: AsyncSession,
    task_id: int,
    task_data: TaskUpdate
):
    task = await get_task_by_id(db, task_id)

    if task is None:
        return None

    update_data = task_data.model_dump(exclude_unset=True)

    if "user_id" in update_data:
        if update_data["user_id"] is None:
            return None

        result = await db.execute(
            select(db_models.User).where(
                db_models.User.id == update_data["user_id"]
            )
        )

        user = result.scalar_one_or_none()

        if user is None:
            return None

    for field in ("title", "status"):
        if field in update_data and update_data[field] is None:
            return None

    for key, value in update_data.items():
        setattr(task, key, value)

    await db.commit()
    await db.refresh(task)

    return task


# DELETE TASK
async def delete_task(
    db: AsyncSession,
    task_id: int
):
    task = await get_task_by_id(db, task_id)

    if task is None:
        return False

    await db.delete(task)
    await db.commit()

    return True