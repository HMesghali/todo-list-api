from typing import Any

from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from app.api.deps import SessionDep
from app.core.security import get_password_hash
from app.models import User, UserCreate, UserPublic

router = APIRouter(prefix='/users', tags=['users'])


@router.post(
	'/', status_code=status.HTTP_201_CREATED, response_model=UserPublic
)
def create_user(*, session: SessionDep, user_in: UserCreate) -> Any:
	# check whether the user with this email exist or not
	membership_statement = select(User).where(User.email == user_in.email)
	user = session.exec(statement=membership_statement).first()
	if user:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail='The user with this email already exists!',
		)

	user = User.model_validate(
		user_in,
		update={'hashed_password': get_password_hash(user_in.password)},
	)
	session.add(user)
	session.commit()
	session.refresh(user)
	return user
