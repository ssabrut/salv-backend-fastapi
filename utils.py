from datetime import datetime, timedelta
from passlib.context import CryptContext
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
import os
from jose import JWTError, jwt
from typing import Annotated
from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from api.crud import user as UserCrud
from dotenv import load_dotenv
from db.models import token as TokenModel
from fastapi.encoders import jsonable_encoder

load_dotenv()

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    finally:
        expiration = payload.get("exp")
        if expiration is None or datetime.utcnow() > datetime.fromtimestamp(expiration):
            raise HTTPException(status_code=401, detail="Token has expired")

        user = await UserCrud.authenticate(db=db, username=token_data.username)
        if user is None:
            raise credentials_exception
        return user


def get_token(request: Request):
    return request.headers["authorization"].split()[-1]


def revoke_token(token: str, db: Session):
    data = {"token": token}
    db_token = TokenModel.Token(**data)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)


def is_token_revoked(token: str, db: Session):
    tokens = db.query(TokenModel.Token).all()
    return token in [t.token for t in tokens]
