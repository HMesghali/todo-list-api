from typing import Any

from fastapi import APIRouter, status

from app.api.deps import CurrentUser, SessionDep
from app.models import Item, ItemCreate, ItemPublic

router = APIRouter(prefix='/todos', tags=['todos'])


# create a todo
@router.post(
	'/', status_code=status.HTTP_201_CREATED, response_model=ItemPublic
)
def create_todo(
	*, session: SessionDep, current_user: CurrentUser, item_in: ItemCreate
) -> Any:
	item = Item.model_validate(item_in, update={'owner_id': current_user.id})
	session.add(item)
	session.commit()
	session.refresh(item)
	return item


# update a todo

# delete a todo

# get a todo

# get todos
