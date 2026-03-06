# Workout Tracker API

A comprehensive workout tracking application built with FastAPI and PostgreSQL that allows users to create, schedule, and manage personalized workout routines.

## Project Overview

This API enables users to:
- Create and manage custom workout plans
- Track exercises with detailed information (sets, reps, weight)
- Schedule workouts for specific dates and times
- Authenticate via email/password or Google OAuth
- Categorize exercises by type and muscle group

## Tech Stack

- **Backend Framework**: FastAPI (Python)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Authentication**: JWT + OAuth 2.0 (Google)
- **Validation**: Pydantic

## Database Schema

### Tables
- **users** - User accounts (email/password + OAuth)
- **exercises** - Exercise library with categories and muscle groups
- **workout_plans** - User-created workout routines
- **workout_exercises** - Junction table linking exercises to plans (with sets/reps/weight)
- **scheduled_workouts** - Calendar of planned workouts

### Key Features
- Exercise categories: strength, cardio, flexibility, balance, sports
- Muscle groups: chest, back, shoulders, arms, legs, core, full_body, glutes
- Cascade deletes (removing a user deletes their plans)
- Timestamp tracking on all entities

## Project Structure

```
workout-tracker/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration settings
│   ├── database.py             # Database connection
│   ├── models/                 # SQLAlchemy models
│   │   ├── user.py
│   │   ├── exercise.py         # ✅ With enums
│   │   ├── workout_plan.py
│   │   ├── workout_exercise.py # ✅ With updated_at
│   │   └── scheduled_workout.py
│   ├── schemas/                # Pydantic schemas
│   │   ├── user.py
│   │   ├── exercise.py
│   │   ├── workout_plan.py
│   │   ├── scheduled_workout.py
│   │   └── auth.py
│   ├── api/                    # API endpoints
│   │   ├── deps.py            # Dependencies (auth, db)
│   │   └── v1/
│   │       ├── auth.py        # ⏳ TODO
│   │       ├── users.py       # ⏳ TODO
│   │       ├── exercises.py   # ⏳ TODO
│   │       ├── workout_plans.py # ⏳ TODO
│   │       └── scheduled_workouts.py # ⏳ TODO
│   ├── core/                  # Core functionality
│   │   ├── security.py        # ⏳ TODO: Password hashing, JWT
│   │   └── oauth.py           # ⏳ TODO: Google OAuth
│   └── services/              # Business logic
│       ├── user_service.py    # ⏳ TODO
│       ├── exercise_service.py # ⏳ TODO
│       ├── workout_service.py # ⏳ TODO
│       └── schedule_service.py # ⏳ TODO
├── alembic/                   # Database migrations
│   └── versions/              # ✅ Initial migration created
├── tests/                     # ⏳ TODO: Test suite
├── .env                       # Environment variables
├── .gitignore
├── requirements.txt
└── README.md
```

## Completed Tasks

- [x] Project structure setup
- [x] Database models with SQLAlchemy
  - [x] User model
  - [x] Exercise model with enums (ExerciseCategory, MuscleGroup)
  - [x] WorkoutPlan model
  - [x] WorkoutExercise model (with updated_at field)
  - [x] ScheduledWorkout model
- [x] Alembic migrations
  - [x] Initial migration created
  - [x] Tables created in PostgreSQL
- [x] Pydantic schemas
  - [x] User schemas (Create, Response, Update, OAuth)
  - [x] Exercise schemas
  - [x] Workout Plan schemas (with nested exercises)
  - [x] Scheduled Workout schemas
  - [x] Auth schemas (Token, Login)

## TODO - Next Steps

### 1. Authentication System (Next Priority)
- [x] Install security packages (`python-jose`, `passlib`)
- [x] Create `app/core/security.py`
  - [x] Password hashing functions
  - [x] JWT token creation/verification
  - [x] Get current user dependency
- [x] Create `app/core/oauth.py`
  - [x] Google OAuth integration
- [x] Create `app/api/v1/auth.py`
  - [x] POST /auth/register - Register with email/password
  - [x] POST /auth/login - Login and get JWT token
  - [X] POST /auth/google - OAuth login
  - [X] POST /auth/refresh - Refresh access token
  <!-- - [ ] POST /auth/logout - Logout user -->

### 2. User Management
- [x] Create `app/services/user_service.py`
- [x] Create `app/api/v1/users.py`
  - [x] GET /users/me - Get current user
  - [x] PUT /users/me - Update profile
  - [x] DELETE /users/me - Delete account

### 3. Exercise Management
- [x] Create `app/services/exercise_service.py`
- [x] Create `app/api/v1/exercises.py`
  - [x] GET /exercises - List exercises (with filters)
  - [x] GET /exercises/{id} - Get exercise details
  - [x] POST /exercises - Create exercise
  - [x] PUT /exercises/{id} - Update exercise
  - [x] DELETE /exercises/{id} - Delete exercise

### 4. Workout Plan Management
- [ ] Create `app/services/workout_service.py`
- [ ] Create `app/api/v1/workout_plans.py`
  - [ ] GET /workout-plans - List user's plans
  - [ ] GET /workout-plans/{id} - Get plan details
  - [ ] POST /workout-plans - Create plan
  - [ ] PUT /workout-plans/{id} - Update plan
  - [ ] DELETE /workout-plans/{id} - Delete plan
  - [ ] POST /workout-plans/{id}/exercises - Add exercise to plan
  - [ ] PUT /workout-plans/{id}/exercises/{exercise_id} - Update exercise in plan
  - [ ] DELETE /workout-plans/{id}/exercises/{exercise_id} - Remove exercise

### 5. Scheduled Workouts
- [ ] Create `app/services/schedule_service.py`
- [ ] Create `app/api/v1/scheduled_workouts.py`
  - [ ] GET /scheduled-workouts - List scheduled workouts
  - [ ] GET /scheduled-workouts/{id} - Get scheduled workout
  - [ ] POST /scheduled-workouts - Schedule a workout
  - [ ] PUT /scheduled-workouts/{id} - Update scheduled workout
  - [ ] DELETE /scheduled-workouts/{id} - Cancel workout
  - [ ] POST /scheduled-workouts/{id}/complete - Mark as completed

### 6. Testing & Documentation
- [ ] Write unit tests for services
- [ ] Write integration tests for API endpoints
- [ ] Add API documentation examples
- [ ] Test OAuth flow end-to-end

### 7. Deployment (Future)
- [ ] Docker containerization
- [ ] Environment-specific configs (dev, staging, prod)
- [ ] CI/CD pipeline
- [ ] Cloud deployment (AWS/GCP/Heroku)

## Environment Variables

Create a `.env` file in the project root:

```env
# Database
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/workout_tracker

# JWT
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# OAuth (to be configured)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback
```

## Getting Started

### Prerequisites
- Python 3.10+
- PostgreSQL 14+
- Virtual environment

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd workout-tracker
```

2. **Create and activate virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up database**
```bash
# Create database
createdb workout_tracker

# Run migrations
alembic upgrade head
```

5. **Run the application**
```bash
uvicorn app.main:app --reload
```

6. **Access the API**
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## API Endpoints (Planned)

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and receive JWT
- `POST /auth/google` - OAuth login
- `POST /auth/refresh` - Refresh token
- `POST /auth/logout` - Logout

### Users
- `GET /users/me` - Get current user
- `PUT /users/me` - Update profile
- `DELETE /users/me` - Delete account

### Exercises
- `GET /exercises` - List exercises
- `POST /exercises` - Create exercise
- `GET /exercises/{id}` - Get exercise
- `PUT /exercises/{id}` - Update exercise
- `DELETE /exercises/{id}` - Delete exercise

### Workout Plans
- `GET /workout-plans` - List plans
- `POST /workout-plans` - Create plan
- `GET /workout-plans/{id}` - Get plan
- `PUT /workout-plans/{id}` - Update plan
- `DELETE /workout-plans/{id}` - Delete plan

### Scheduled Workouts
- `GET /scheduled-workouts` - List scheduled
- `POST /scheduled-workouts` - Schedule workout
- `GET /scheduled-workouts/{id}` - Get scheduled
- `PUT /scheduled-workouts/{id}` - Update scheduled
- `POST /scheduled-workouts/{id}/complete` - Mark complete

## Custom Modifications

### Exercise Model Enhancements
- Added `ExerciseCategory` enum with 5 categories
- Added `MuscleGroup` enum with 8 muscle groups
- Both enums ensure data consistency

### WorkoutExercise Model Enhancement
- Added `updated_at` field to track modifications to exercise parameters

## Future Enhancements

- Progress tracking and analytics
- Exercise video/image uploads
- Social features (share workouts, follow users)
- Workout templates library
- Rest timer functionality
- Personal records (PR) tracking
- Body measurements tracking
- Nutrition tracking integration
- Mobile app (React Native/Flutter)

<!-- ## 📄 License

[Your chosen license]

## 👤 Author

[Your name] -->

---

**Current Status**: Database and schemas complete. Next: Authentication system.


<!-- test@example.com
mypassword123 -->