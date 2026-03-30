# Workout Tracker — Claude Context

## What this project is
A REST API for tracking personalized workouts. Users can register, create workout plans, manage an exercise library, schedule sessions on a calendar, and mark workouts as completed. A Next.js frontend is planned but not started yet.

## Tech Stack
- **Backend**: FastAPI (Python 3.10+)
- **Database**: PostgreSQL 14+ via SQLAlchemy ORM
- **Migrations**: Alembic
- **Auth**: JWT (python-jose) + Google OAuth 2.0
- **Validation**: Pydantic v2
- **Frontend (planned)**: Next.js + TypeScript + React

## Project Structure
```
app/
├── main.py              # FastAPI app entry point
├── config.py            # Settings from .env
├── database.py          # DB session setup
├── models/              # SQLAlchemy models
├── schemas/             # Pydantic schemas
├── api/
│   ├── deps.py          # Shared dependencies (get_db, get_current_user)
│   └── v1/              # All HTTP endpoint routers
├── core/
│   ├── security.py      # Password hashing, JWT
│   └── oauth.py         # Google OAuth
└── services/            # Business logic (no HTTP here)
```

## Architecture Rules
- **Services handle business logic** — endpoints only handle HTTP (request parsing, response formatting, status codes)
- **No business logic in endpoints** — always delegate to the service layer
- **All endpoints under `/api/v1/`** — versioned for future compatibility
- **Pydantic schemas for everything** — never return raw SQLAlchemy models
- **Dependency injection via `deps.py`** — use `get_db` and `get_current_user` consistently

## Database Models

### Tables
- `users` — email/password + OAuth accounts
- `exercises` — shared exercise library
- `workout_plans` — user-created routines
- `workout_exercises` — junction: exercise in a plan (sets, reps, weight, updated_at)
- `scheduled_workouts` — calendar entries linking user + plan + date

### Key rules
- All models have `created_at` and `updated_at` timestamps
- Cascade deletes: removing a user removes all their plans and scheduled workouts
- `ExerciseCategory` enum: strength, cardio, flexibility, balance, sports
- `MuscleGroup` enum: chest, back, shoulders, arms, legs, core, full_body, glutes

## Auth Flow
- Register/login returns `access_token` (JWT, 30min) + `refresh_token` (7 days)
- Google OAuth via `/auth/google`
- All protected routes use `get_current_user` dependency from `deps.py`

## Coding Conventions
- Snake_case for Python variables, functions, and file names
- Pydantic schema naming: `EntityCreate`, `EntityResponse`, `EntityUpdate`
- Service functions named: `get_entity`, `create_entity`, `update_entity`, `delete_entity`
- Endpoints return Pydantic response schemas, never raw dicts
- Use `HTTPException` for all error responses with appropriate status codes

## Current Status
| Module | Models | Schemas | Service | Endpoints |
|---|---|---|---|---|
| Auth | ✅ | ✅ | ✅ | ✅ |
| Users | ✅ | ✅ | ✅ | ✅ |
| Exercises | ✅ | ✅ | ✅ | ✅ |
| Workout Plans | ✅ | ✅ | ⏳ TODO | ⏳ TODO |
| Scheduled Workouts | ✅ | ✅ | ⏳ TODO | ⏳ TODO |

## What to build next
1. `app/services/workout_service.py` — CRUD for workout plans + adding/removing/updating exercises in a plan
2. `app/api/v1/workout_plans.py` — endpoints for the above
3. `app/services/schedule_service.py` — schedule, update, cancel, complete workouts
4. `app/api/v1/scheduled_workouts.py` — endpoints for the above
5. `tests/` — unit tests for services, integration tests for endpoints

## Environment Variables (required)
```
DATABASE_URL=postgresql://...
SECRET_KEY=...
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
GOOGLE_REDIRECT_URI=...
```

## Future Scope (not started)
- Frontend: Next.js + TypeScript + React
- Docker + CI/CD
- Progress analytics, PR tracking, body measurements
- Social features, workout templates, nutrition integration
