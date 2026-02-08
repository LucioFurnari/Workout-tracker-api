from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import Optional, List
from app.models.exercise import Exercise, ExerciseCategory, MuscleGroup
from app.schemas.exercise import ExerciseCreate, ExerciseUpdate


def get_exercise_by_id(db: Session, exercise_id: int) -> Optional[Exercise]:
    """Get a single exercise by ID"""
    return db.query(Exercise).filter(Exercise.id == exercise_id).first()


def get_exercises(
    db: Session,
    current_user_id: int,
    skip: int = 0,
    limit: int = 100,
    only_mine: bool = False,
    category: Optional[ExerciseCategory] = None,
    muscle_group: Optional[MuscleGroup] = None,
    is_public: Optional[bool] = None,
    search: Optional[str] = None,
    sort_by: str = "created_at",
    sort_order: str = "desc"
) -> tuple[List[Exercise], int]:
    """
    Get exercises with filters and pagination.
    Returns tuple of (exercises, total_count)
    """
    query = db.query(Exercise)
    
    # Default: Show user's exercises + public exercises
    if only_mine:
        query = query.filter(Exercise.created_by == current_user_id)
    else:
        query = query.filter(
            or_(
                Exercise.created_by == current_user_id,
                Exercise.is_public == True
            )
        )
    
    # Apply filters
    if category:
        query = query.filter(Exercise.category == category)
    
    if muscle_group:
        query = query.filter(Exercise.muscle_group == muscle_group)
    
    if is_public is not None:
        query = query.filter(Exercise.is_public == is_public)
    
    if search:
        search_filter = or_(
            Exercise.name.ilike(f"%{search}%"),
            Exercise.description.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    # Get total count before pagination
    total_count = query.count()
    
    # Apply sorting
    if hasattr(Exercise, sort_by):
        sort_column = getattr(Exercise, sort_by)
        if sort_order.lower() == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())
    
    # Apply pagination
    exercises = query.offset(skip).limit(limit).all()
    
    return exercises, total_count


def create_exercise(db: Session, exercise: ExerciseCreate, user_id: int) -> Exercise:
    """Create a new exercise"""
    db_exercise = Exercise(
        **exercise.model_dump(),
        created_by=user_id
    )
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise


def update_exercise(
    db: Session,
    exercise_id: int,
    exercise_update: ExerciseUpdate,
    user_id: int
) -> Optional[Exercise]:
    """Update an exercise (only if user owns it)"""
    db_exercise = db.query(Exercise).filter(
        Exercise.id == exercise_id,
        Exercise.created_by == user_id
    ).first()
    
    if not db_exercise:
        return None
    
    update_data = exercise_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_exercise, field, value)
    
    db.commit()
    db.refresh(db_exercise)
    return db_exercise


def delete_exercise(db: Session, exercise_id: int, user_id: int) -> bool:
    """Delete an exercise (only if user owns it)"""
    db_exercise = db.query(Exercise).filter(
        Exercise.id == exercise_id,
        Exercise.created_by == user_id
    ).first()
    
    if not db_exercise:
        return False
    
    db.delete(db_exercise)
    db.commit()
    return True