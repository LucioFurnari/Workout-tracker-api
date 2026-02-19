from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.exercise import ExerciseCategory, MuscleGroup
from app.schemas.exercise import (
    ExerciseCreate,
    ExerciseResponse,
    ExerciseUpdate,
    ExerciseListResponse
)
from app.services.exercise_service import (
    get_exercises,
    get_exercise_by_id,
    create_exercise,
    update_exercise,
    delete_exercise
)

router = APIRouter()


@router.get("", response_model=ExerciseListResponse)
def list_exercises(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Max number of records to return"),
    only_mine: bool = Query(False, description="Show only exercises created by me"),
    category: Optional[ExerciseCategory] = Query(None, description="Filter by exercise category"),
    muscle_group: Optional[MuscleGroup] = Query(None, description="Filter by muscle group"),
    is_public: Optional[bool] = Query(None, description="Filter by public/private status"),
    search: Optional[str] = Query(None, min_length=1, description="Search in name and description"),
    sort_by: str = Query("created_at", description="Field to sort by (name, created_at, category)"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="Sort order: asc or desc"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get list of exercises with filters and pagination.
    
    By default, returns:
    - All exercises created by the current user
    - All public exercises created by other users
    
    Use filters to refine results:
    - only_mine: Show only your exercises
    - category: Filter by exercise type (strength, cardio, etc.)
    - muscle_group: Filter by target muscle
    - search: Search in exercise name and description
    """
    exercises, total = get_exercises(
        db=db,
        current_user_id=current_user.id,
        skip=skip,
        limit=limit,
        only_mine=only_mine,
        category=category,
        muscle_group=muscle_group,
        is_public=is_public,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order
    )
    
    return ExerciseListResponse(
        exercises=exercises,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/{exercise_id}", response_model=ExerciseResponse)
def get_exercise(
    exercise_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific exercise by ID.
    
    You can only view:
    - Exercises you created
    - Public exercises created by others
    """
    exercise = get_exercise_by_id(db, exercise_id)
    
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercise not found"
        )
    
    # Check if user has access to this exercise
    if exercise.created_by != current_user.id and not exercise.is_public:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view this exercise"
        )
    
    return exercise


@router.post("", response_model=ExerciseResponse, status_code=status.HTTP_201_CREATED)
def create_new_exercise(
    exercise: ExerciseCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new exercise.
    
    The exercise will be created with you as the owner.
    Set is_public=true to share it with other users.
    """
    return create_exercise(db, exercise, current_user.id)


@router.put("/{exercise_id}", response_model=ExerciseResponse)
def update_existing_exercise(
    exercise_id: int,
    exercise_update: ExerciseUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update an exercise.
    
    You can only update exercises you created.
    """
    updated_exercise = update_exercise(db, exercise_id, exercise_update, current_user.id)
    
    if not updated_exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercise not found or you don't have permission to update it"
        )
    
    return updated_exercise


@router.delete("/{exercise_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_exercise(
    exercise_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete an exercise.
    
    You can only delete exercises you created.
    Note: This will fail if the exercise is used in any workout plans.
    """
    success = delete_exercise(db, exercise_id, current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercise not found or you don't have permission to delete it"
        )
    
    return None