from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List
from app.models.exercise import ExerciseCategory, MuscleGroup

class ExerciseBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: ExerciseCategory
    muscle_group: MuscleGroup

class ExerciseCreate(ExerciseBase):
    is_public: bool = False

class ExerciseUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[ExerciseCategory] = None
    muscle_group: Optional[MuscleGroup] = None
    is_public: Optional[bool] = None

class ExerciseResponse(ExerciseBase):
    id: int
    created_by: Optional[int] = None
    is_public: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

# Pagination response
class ExerciseListResponse(BaseModel):
    exercises: List[ExerciseResponse]
    total: int
    skip: int
    limit: int
    
    @property
    def has_more(self) -> bool:
        """Check if there are more results"""
        return self.skip + self.limit < self.total