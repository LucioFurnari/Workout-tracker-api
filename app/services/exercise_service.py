from sqlalchemy.orm import Session
from app.models.exercise import Exercise

from typing import Optional


def get_exercise_list(db: Session, filter: str) -> Optional[Exercise]:
  return db.query(Exercise).filter
