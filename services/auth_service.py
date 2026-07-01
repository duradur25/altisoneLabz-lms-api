from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.lms_models import User
from core.security import verify_pw, create_access_token, create_refresh_token, decode_token


def login(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=401, detail="Email or password invalid")

    if not verify_pw(password, user.password):
        raise HTTPException(status_code=401, detail="Email or password invalid")

    payload = {
        "sub": str(user.id),
        "role": user.role
    }

    access_token = create_access_token(payload)
    refresh_token = create_refresh_token(payload)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


def refresh_token(db: Session, token: str):
    payload = decode_token(token)

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="this token is not refresh token")

    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == int(user_id)).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    # buat access token baru
    new_access_token = create_access_token({
        "sub": str(user.id),
        "role": user.role
    })

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }


def get_me(current_user: User):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "role": current_user.role
    }