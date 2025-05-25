from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app import crud
from app.api.deps import SessionDep
from app.core.security import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from app.models import Token

router = APIRouter(tags=['login'])


@router.post('/token')
def login_access_token(
	*,
	session: SessionDep,
	form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
	user = crud.authenticate(
		session=session, email=form_data.username, password=form_data.password
	)
	if not user:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail='Incorrect email or password',
		)
	elif not user.is_active:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST, detail='Inactive user'
		)
	return Token(
		access_token=create_access_token(
			user.id, expires_delta=timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
		)
	)
