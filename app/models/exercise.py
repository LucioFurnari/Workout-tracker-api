from sqlalchemy import Column, Integer, String, Text, Enum, Boolean, DateTime, ForeignKey
import enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class ExerciseCategory(enum.Enum):
  STRENGTH = "strength"
  CARDIO = "cardio"
  FLEXIBILITY = "flexibility"
  BALANCE = "balance"
  SPORTS = "sports"

class MuscleGroup(enum.Enum):
  CHEST = "chest"
  BACK = "back"
  SHOULDERS = "shoulders"
  ARMS = "arms"
  LEGS = "legs"
  CORE = "core"
  FULL_BODY = "full_body"
  GLUTES = "glutes"


class Exercise(Base):
  __tablename__ = "exercises"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String(255), nullable=False)
  description = Column(Text, nullable=True)
  category = Column(Enum(ExerciseCategory), nullable=False)
  muscle_group = Column(Enum(MuscleGroup), nullable=False)
  created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
  is_public = Column(Boolean, default=False)
  created_at = Column(DateTime(timezone=True), server_default=func.now())
  updated_at = Column(DateTime(timezone=True), onupdate=func.now())

  # Relationship to user who created it
  creator = relationship("User", backref="exercises")

