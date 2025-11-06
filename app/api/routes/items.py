import uuid
from typing import Any

from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from app.api.deps import CurrentUser, SessionDep
from app.models import Item, ItemCreate, ItemPublic, ItemUpdate

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
@router.patch(
	'/{id}', status_code=status.HTTP_200_OK, response_model=ItemPublic
)
def update_todo(
	*,
	session: SessionDep,
	current_user: CurrentUser,
	id: uuid.UUID,
	item_in: ItemUpdate,
) -> Any:
	item = session.get(Item, id)
	if not item:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND, detail='Item not found!'
		)
	if current_user.id != item.owner_id:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST, detail='Not allowed!'
		)
	update_dict = item_in.model_dump(exclude_unset=True)
	item.sqlmodel_update(update_dict)
	session.add(item)
	session.commit()
	session.refresh(item)
	return item


# delete a todo
@router.delete('/{id}', status_code=status.HTTP_200_OK)
def delete_todo(
	*, session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Any:
	item = session.get(Item, id)
	if not item:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND, detail='Item not found!'
		)
	if item.owner_id != current_user.id:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST, detail='Not allowed!'
		)
	session.delete(item)
	session.commit()
	return {'Message': 'Item Deleted Successfully'}


@router.get(
	'/', status_code=status.HTTP_200_OK, response_model=list[ItemPublic]
)
def read_items(
	*,
	session: SessionDep,
	current_user: CurrentUser,
	skip: int = 0,
	limit: int = 100,
) -> Any:
	statement = (
		select(Item)
		.where(Item.owner_id == current_user.id)
		.offset(skip)
		.limit(limit)
	)
	items = session.exec(statement).all()
	return items


# get a todo
@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=ItemPublic)
def read_item(
	*, session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Any:
	item = session.get(Item, id)
	if not item:
		raise HTTPException(status_code=404, detail='Item not found')
	if not current_user.is_superuser and (item.owner_id != current_user.id):
		raise HTTPException(status_code=400, detail='Not enough permissions')
	return item
