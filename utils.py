from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_context.hash(password)
