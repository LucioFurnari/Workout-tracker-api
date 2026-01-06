from sqlalchemy import Column, Integer, String, Text, Date, Time, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class ScheduleWorkout(Base):
  __tablename__ = "scheduled_workouts"

  id = Column(Integer, primary_key=True, index=True)
  user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
  workout_plan_id = Column(Integer, ForeignKey("workout_plans.id", ondelete="CASCADE"), nullable=False)
  scheduled_date = Column(Date, nullable=False)
  scheduled_time = Column(Time, nullable=True)
  status = Column(String(50), default="scheduled")  # scheduled, completed, cancelled
  completed_at = Column(DateTime(timezone=True), nullable=True)
  notes = Column(Text, nullable=True)
  created_at = Column(DateTime(timezone=True), server_default=func.now())
  updated_at = Column(DateTime(timezone=True), onupdate=func.now())

  # Relationships
  user = relationship("User", backref="scheduled_workouts")
  workout_plan = relationship("WorkoutPlan", backref="scheduled_workouts")