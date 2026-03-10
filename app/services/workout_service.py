from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.workout_plan import WorkoutPlan, WorkoutPlanExercise
from app.schemas.workout_plan import (
    WorkoutPlanCreate,
    WorkoutPlanUpdate,
    WorkoutExerciseCreate,
    WorkoutExerciseUpdate
)


def get_workout_plan_by_id(db: Session, plan_id: int) -> Optional[WorkoutPlan]:
    """Get a single workout plan by ID"""
    return db.query(WorkoutPlan).filter(WorkoutPlan.id == plan_id).first()


def get_workout_plans(
    db: Session,
    current_user_id: int,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    sort_by: str = "created_at",
    sort_order: str = "desc"
) -> tuple[List[WorkoutPlan], int]:
    """
    Get workout plans for the current user with pagination.
    Returns tuple of (plans, total_count)
    """
    query = db.query(WorkoutPlan).filter(WorkoutPlan.created_by == current_user_id)

    if search:
        query = query.filter(WorkoutPlan.name.ilike(f"%{search}%"))

    total_count = query.count()

    if hasattr(WorkoutPlan, sort_by):
        sort_column = getattr(WorkoutPlan, sort_by)
        if sort_order.lower() == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())

    plans = query.offset(skip).limit(limit).all()
    return plans, total_count


def create_workout_plan(db: Session, plan: WorkoutPlanCreate, user_id: int) -> WorkoutPlan:
    """Create a new workout plan"""
    db_plan = WorkoutPlan(**plan.model_dump(), created_by=user_id)
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan


def update_workout_plan(
    db: Session,
    plan_id: int,
    plan_update: WorkoutPlanUpdate,
    user_id: int
) -> Optional[WorkoutPlan]:
    """Update a workout plan (only if user owns it)"""
    db_plan = db.query(WorkoutPlan).filter(
        WorkoutPlan.id == plan_id,
        WorkoutPlan.created_by == user_id
    ).first()

    if not db_plan:
        return None

    update_data = plan_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_plan, field, value)

    db.commit()
    db.refresh(db_plan)
    return db_plan


def delete_workout_plan(db: Session, plan_id: int, user_id: int) -> bool:
    """Delete a workout plan (only if user owns it)"""
    db_plan = db.query(WorkoutPlan).filter(
        WorkoutPlan.id == plan_id,
        WorkoutPlan.created_by == user_id
    ).first()

    if not db_plan:
        return False

    db.delete(db_plan)
    db.commit()
    return True


# --- Workout Plan Exercise management ---

def get_plan_exercise(db: Session, plan_id: int, exercise_id: int) -> Optional[WorkoutPlanExercise]:
    """Get a specific exercise entry within a workout plan"""
    return db.query(WorkoutPlanExercise).filter(
        WorkoutPlanExercise.workout_plan_id == plan_id,
        WorkoutPlanExercise.exercise_id == exercise_id
    ).first()


def add_exercise_to_plan(
    db: Session,
    plan_id: int,
    exercise_data: WorkoutExerciseCreate
) -> WorkoutPlanExercise:
    """Add an exercise to a workout plan"""
    db_plan_exercise = WorkoutPlanExercise(
        workout_plan_id=plan_id,
        **exercise_data.model_dump()
    )
    db.add(db_plan_exercise)
    db.commit()
    db.refresh(db_plan_exercise)
    return db_plan_exercise


def update_exercise_in_plan(
    db: Session,
    plan_id: int,
    exercise_id: int,
    exercise_update: WorkoutExerciseUpdate
) -> Optional[WorkoutPlanExercise]:
    """Update an exercise entry within a workout plan"""
    db_plan_exercise = get_plan_exercise(db, plan_id, exercise_id)

    if not db_plan_exercise:
        return None

    update_data = exercise_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_plan_exercise, field, value)

    db.commit()
    db.refresh(db_plan_exercise)
    return db_plan_exercise


def remove_exercise_from_plan(db: Session, plan_id: int, exercise_id: int) -> bool:
    """Remove an exercise from a workout plan"""
    db_plan_exercise = get_plan_exercise(db, plan_id, exercise_id)

    if not db_plan_exercise:
        return False

    db.delete(db_plan_exercise)
    db.commit()
    return True