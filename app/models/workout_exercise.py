from sqlalchemy import Column, Integer, Numeric, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class WorkoutExercise(Base):
  __tablename__ = "workout_exercises"

  id = Column(Integer, primary_key=True, index=True)
  workout_plan_id = Column(Integer, ForeignKey("workout_plans.id", ondelete="CASCADE"), nullable=False)
  exercise_id = Column(Integer, ForeignKey("exercises.id", ondelete="CASCADE"), nullable=False)
  sets = Column(Integer, nullable=False)
  repetitions = Column(Integer, nullable=False)
  weight = Column(Numeric(10, 2), nullable=True)  # Optional, for weighted exercises
  order_index = Column(Integer, nullable=False)  # Order of exercises in the plan
  notes = Column(Text, nullable=True)
  created_at = Column(DateTime(timezone=True), server_default=func.now())
  updated_at = Column(DateTime(timezone=True), onupdate=func.now())

  # Relationships
  workout_plan = relationship("WorkoutPlan", back_populates="exercises")
  exercise = relationship("Exercise")