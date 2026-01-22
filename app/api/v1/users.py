from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.schemas.user import UserResponse, UserUpdate
from app.services.user_service import update_user, delete_user
from app.models.user import User

router = APIRouter()

@router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
  return current_user

@router.put("/me", response_model=UserResponse)
def update_current_user_profile(
  user_update: UserUpdate,
  current_user: User = Depends(get_current_user),
  db: Session = Depends(get_db)
):
  updated_user = update_user(db, current_user.id, user_update)
  if not updated_user:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="User not found"
    )
  return updated_user

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_current_user_account(
  current_user: User = Depends(get_current_user),
  db: Session = Depends(get_db)
):
  success = delete_user(db, current_user.id)
  if not success:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="User not found"
    )
  return None