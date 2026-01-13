from pydantic import BaseModel, ConfigDict
from datetime import datetime, date, time
from typing import Optional

class ScheduleWorkoutBase(BaseModel):
  workout_plan_id: int
  scheduled_date: date
  scheduled_time: Optional[time] = None
  notes: Optional[str] = None

class ScheduledWorkoutCreate(ScheduleWorkoutBase):
  pass

class ScheduledWorkoutUpdate(BaseModel):
  scheduled_date: Optional[date] = None
  scheduled_time: Optional[time] = None
  status: Optional[str] = None
  notes: Optional[str] = None

class ScheduledWorkoutResponse(ScheduleWorkoutBase):
  id: int
  user_id: int
  status: str
  completed_at: Optional[datetime] = None
  created_at: datetime
  updated_at: Optional[datetime] = None

  model_config = ConfigDict(from_attributes=True)

class ScheduledWorkoutComplete(BaseModel):
  notes: Optional[str] = None