from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List
from decimal import Decimal

# Schema for exercise within a workout plan
class WorkoutExerciseBase(BaseModel):
  exercise_id: int
  sets: int
  repetitions: int
  weight: Optional[str] = None
  order_index: int
  notes: Optional[str] = None

class WorkoutExerciseCreate(WorkoutExerciseBase):
  pass

class WorkoutExerciseUpdate(BaseModel):
  sets: Optional[int] = None
  repetitions: Optional[int] = None
  weight: Optional[Decimal] = None
  order_index: Optional[int] = None
  notes:  Optional[str] = None

class WorkoutExerciseResponse(WorkoutExerciseBase):
  id: int
  workout_plan_id: int
  created_at: datetime
  updated_at: Optional[datetime] = None

  mode_config = ConfigDict(from_attributes=True)

# Workout Plan schemas
class WorkoutPlanBase(BaseModel):
  name: str
  description: Optional[str] = None

class WorkoutPlanCreate(WorkoutPlanBase):
  exercise: List[WorkoutExerciseCreate] = []

class WorkoutPlanUpdate(BaseModel):
  name: Optional[str] = None
  description: Optional[str] = None

class WorkoutPlanResponse(WorkoutPlanBase):
  id: int
  user_id: int
  created_at: datetime
  updated_at: Optional[datetime] = None
  exercise: List[WorkoutExerciseResponse] = None

  model_config = ConfigDict(from_attributes=True)

