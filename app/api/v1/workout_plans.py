from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.workout_plan import (
    WorkoutPlanCreate,
    WorkoutPlanUpdate,
    WorkoutPlanResponse,
    WorkoutExerciseCreate,
    WorkoutExerciseUpdate,
    WorkoutExerciseResponse
)
from app.services.workout_service import (
    get_workout_plans,
    get_workout_plan_by_id,
    create_workout_plan,
    update_workout_plan,
    delete_workout_plan,
    add_exercise_to_plan,
    update_exercise_in_plan,
    remove_exercise_from_plan,
    get_workout_exercise
)

router = APIRouter()


# --- Helper ---

def _get_owned_plan(db: Session, plan_id: int, user_id: int):
    """Fetch a plan and verify ownership, raising appropriate HTTP errors."""
    plan = get_workout_plan_by_id(db, plan_id)
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout plan not found"
        )
    if plan.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this workout plan"
        )
    return plan


# --- Workout Plan CRUD ---

@router.get("", response_model=List[WorkoutPlanResponse])
def list_workout_plans(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Max number of records to return"),
    search: Optional[str] = Query(None, min_length=1, description="Search in plan name"),
    sort_by: str = Query("created_at", description="Field to sort by (name, created_at)"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="Sort order: asc or desc"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all workout plans belonging to the current user.

    Supports search by name, sorting, and pagination.
    """
    plans, _ = get_workout_plans(
        db=db,
        current_user_id=current_user.id,
        skip=skip,
        limit=limit,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order
    )
    return plans


@router.get("/{plan_id}", response_model=WorkoutPlanResponse)
def get_workout_plan(
    plan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific workout plan by ID.

    You can only view plans you created.
    """
    return _get_owned_plan(db, plan_id, current_user.id)


@router.post("", response_model=WorkoutPlanResponse, status_code=status.HTTP_201_CREATED)
def create_new_workout_plan(
    plan: WorkoutPlanCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new workout plan.

    You can optionally include a list of exercises at creation time.
    """
    return create_workout_plan(db, plan, current_user.id)


@router.put("/{plan_id}", response_model=WorkoutPlanResponse)
def update_existing_workout_plan(
    plan_id: int,
    plan_update: WorkoutPlanUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a workout plan's name or description.

    You can only update plans you created.
    """
    updated_plan = update_workout_plan(db, plan_id, plan_update, current_user.id)

    if not updated_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout plan not found or you don't have permission to update it"
        )
    return updated_plan


@router.delete("/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_workout_plan(
    plan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a workout plan and all its exercises.

    You can only delete plans you created.
    """
    success = delete_workout_plan(db, plan_id, current_user.id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout plan not found or you don't have permission to delete it"
        )
    return None


# --- Exercises within a Plan ---

@router.post("/{plan_id}/exercises", response_model=WorkoutExerciseResponse, status_code=status.HTTP_201_CREATED)
def add_exercise(
    plan_id: int,
    exercise_data: WorkoutExerciseCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Add an exercise to a workout plan.

    You can only modify plans you created.
    """
    _get_owned_plan(db, plan_id, current_user.id)

    existing = get_workout_exercise(db, plan_id, exercise_data.exercise_id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This exercise is already in the workout plan"
        )

    return add_exercise_to_plan(db, plan_id, exercise_data)


@router.put("/{plan_id}/exercises/{exercise_id}", response_model=WorkoutExerciseResponse)
def update_exercise(
    plan_id: int,
    exercise_id: int,
    exercise_update: WorkoutExerciseUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update an exercise within a workout plan (sets, reps, weight, order, notes).

    You can only modify plans you created.
    """
    _get_owned_plan(db, plan_id, current_user.id)

    updated = update_exercise_in_plan(db, plan_id, exercise_id, exercise_update)

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercise not found in this workout plan"
        )
    return updated


@router.delete("/{plan_id}/exercises/{exercise_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_exercise(
    plan_id: int,
    exercise_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Remove an exercise from a workout plan.

    You can only modify plans you created.
    """
    _get_owned_plan(db, plan_id, current_user.id)

    success = remove_exercise_from_plan(db, plan_id, exercise_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercise not found in this workout plan"
        )
    return None
