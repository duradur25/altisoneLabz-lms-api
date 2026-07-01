from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.config import get_db
from api.deps import get_current_user
from services.auth_service import login, refresh_token, get_me
from models.lms_models import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login")
def login_endpoint(email: str, password: str, db: Session = Depends(get_db)):
    return login(db, email, password)


@router.post("/refresh")
def refresh_endpoint(token: str, db: Session = Depends(get_db)):
    return refresh_token(db, token)


@router.get("/me")
def me_endpoint(current_user: User = Depends(get_current_user)):
    return get_me(current_user)