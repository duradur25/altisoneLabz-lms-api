from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from database.config import get_db
from models.lms_models import User
from core.security import decode_token 


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
                ) -> User:
    payload= decode_token(token)
    
    if payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="This token is not access token")

    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == int(user_id)).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can access")
    return current_user


def require_mentor(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "mentor":
        raise HTTPException(status_code=403, detail="Only mentor can access")
    return current_user