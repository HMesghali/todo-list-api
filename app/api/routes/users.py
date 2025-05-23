from typing import Any

from fastapi import APIRouter, HTTPException, status

from app import crud
from app.api.deps import SessionDep
from app.models import UserCreate, UserPublic

router = APIRouter(prefix='/users', tags=['users'])


@router.post(
	'/',
	status_code=status.HTTP_201_CREATED,
	response_model=UserPublic,
)
def create_user(*, session: SessionDep, user_in: UserCreate) -> Any:
	# check whether the user with this email exist or not
	user = crud.get_user_by_email(session=session, email=user_in.email)
	if user:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail='The user with this email already exists!',
		)

	user = crud.create_user(session=session, user_create=user_in)
	return user
