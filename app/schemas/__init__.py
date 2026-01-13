from app.schemas.user import UserCreate, UserResponse, UserUpdate, UserOAuthCreate
from app.schemas.exercise import ExerciseCreate, ExerciseResponse, ExerciseUpdate
from app.schemas.workout_plan import (
    WorkoutPlanCreate, 
    WorkoutPlanResponse, 
    WorkoutPlanUpdate,
    WorkoutExerciseCreate,
    WorkoutExerciseResponse,
    WorkoutExerciseUpdate
)
from app.schemas.scheduled_workout import (
    ScheduledWorkoutCreate,
    ScheduledWorkoutResponse,
    ScheduledWorkoutUpdate,
    ScheduledWorkoutComplete
)
from app.schemas.auth import Token, TokenData, LoginRequest, GoogleAuthRequest