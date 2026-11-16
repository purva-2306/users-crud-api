
from typing import Literal

from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.async_database import get_async_db
from app.models.user import TaskCreate, TaskUpdate, TaskResponse
from app.models import db_models
from app.services import async_task_service
from app.core.dependencies import get_current_user, require_role


router = APIRouter(
    prefix="/api/v1/tasks",
    tags=["Tasks"]
)


# CREATE TASK - TEACHER ONLY
@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_task(
    task: TaskCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: db_models.User = Depends(require_role("teacher"))
):
    new_task = await async_task_service.create_task(db, task)

    if new_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return new_task


# GET ALL TASKS WITH PAGINATION, SEARCH AND FILTERS
@router.get("/", response_model=list[TaskResponse])
async def get_all_tasks(
    task_status: Literal["pending", "in progress", "done"] | None = None,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    search: str | None = Query(default=None, min_length=1, max_length=100),
    assigned_user_id: int | None = Query(default=None, gt=0),
    db: AsyncSession = Depends(get_async_db),
    current_user: db_models.User = Depends(get_current_user)
):
    if current_user.role == "teacher":
        return await async_task_service.get_all_tasks(
            db,
            task_status=task_status,
            page=page,
            limit=limit,
            search=search,
            assigned_user_id=assigned_user_id
        )

    return await async_task_service.get_all_tasks(
        db,
        task_status=task_status,
        user_id=current_user.id,
        page=page,
        limit=limit,
        search=search
    )


# GET TASK BY ID
@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: db_models.User = Depends(get_current_user)
):
    task = await async_task_service.get_task_by_id(db, task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    if current_user.role != "teacher" and task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own tasks"
        )

    return task


# UPDATE TASK
@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task: TaskUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: db_models.User = Depends(get_current_user)
):
    existing_task = await async_task_service.get_task_by_id(
        db, task_id
    )

    if existing_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    if current_user.role == "student":
        if existing_task.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update your own tasks"
            )

        allowed_fields = {"status", "work_notes"}
        provided_fields = task.model_fields_set

        if not provided_fields or not provided_fields.issubset(allowed_fields):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Students can only update task status and work notes"
            )

        if "status" in provided_fields and task.status is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Task status cannot be empty"
            )

    updated_task = await async_task_service.update_task(
        db, task_id, task
    )

    if updated_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task or assigned user not found"
        )

    return updated_task


# DELETE TASK - TEACHER ONLY
@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: db_models.User = Depends(require_role("teacher"))
):
    deleted = await async_task_service.delete_task(db, task_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return None