from jose import jwt, JWTError
from datetime import datetime, timedelta
from database.config import SECRET_KEY, ALGORITHM
from fastapi import HTTPException
from database.config import ACCESS_TOKEN_EXPIRED_MINUTES, REFRESH_TOKEN_EXPIRED_DAYS

#JWT
def create_token(data: dict, expires_delta: timedelta, token_type: str) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire, "type": token_type})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="token isn't valid yet"
        )
    
def create_access_token(data: dict) -> str:
    return create_token(data, timedelta(minutes=ACCESS_TOKEN_EXPIRED_MINUTES), "access")

def create_refresh_token(data: dict) -> str:
    return create_token(data, timedelta(days=REFRESH_TOKEN_EXPIRED_DAYS), "refresh")


#Hash
from passlib.context import CryptContext

pw_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_pw(password):
    return pw_context.hash(password)

def verify_pw(password, hashed_pw):
    return pw_context.verify(password, hashed_pw)

