from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

SECRET_KEY = 'bdafebc1513573af9e56b278ac1200758f0bdf8485bcb95ec6fa59ea14f74e05'
SECURITY_ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(subject: str | Any, expires_delta: timedelta) -> str:
	expire = datetime.now(UTC) + expires_delta
	to_encode = {'exp': expire, 'sub': str(subject)}
	encoded_jwt = jwt.encode(
		to_encode, SECRET_KEY, algorithm=SECURITY_ALGORITHM
	)
	return encoded_jwt


def get_password_hash(password) -> str:
	return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
	return pwd_context.verify(plain_password, hashed_password)
