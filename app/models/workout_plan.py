from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class WorkoutPlan(Base):
  __tablename__ = "workout_plans"

  id = Column(Integer, primary_key=True, index=True)
  user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
  name = Column(String(255), nullable=False)
  description = Column(Text, nullable=True)
  created_at = Column(DateTime(timezone=True), server_default=func.now())
  updated_at = Column(DateTime(timezone=True), onupdate=func.now())

  # Relationship
  user = relationship("User", backref="workout_plans")
  exercises = relationship("WorkoutExercise", back_populates="workout_plan", cascade="all, delete-orphan")