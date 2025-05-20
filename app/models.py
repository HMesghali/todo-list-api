import uuid

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


# ----------------------
# USER
# ----------------------
# User's shared properties
class UserBase(SQLModel):
	email: EmailStr = Field(unique=True, index=True, max_length=255)
	full_name: str | None = Field(default=None, max_length=255)
	is_active: bool = True
	is_superuser: bool = False


# User's create model
class UserCreate(UserBase):
	password: str = Field(min_length=8, max_length=40)


# User's database model
class User(UserBase, table=True):
	id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
	hashed_password: str
	items: list['Item'] = Relationship(
		back_populates='owner', cascade_delete=True
	)


# User's public model
class UserPublic(UserBase):
	id: uuid.UUID


# Users' public model
class UsersPublic(SQLModel):
	data: list[UserPublic]
	count: int


# ----------------------
# Item
# ----------------------
# Todo's shared properties
class ItemBase(SQLModel):
	title: str = Field(min_length=1, max_length=255)
	description: str | None = Field(default=None, max_length=255)


# Todo's create model
class ItemCreate(ItemBase):
	pass


# Todo's update model
class ItemUpdate(ItemBase):
	title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore
	description: str | None = Field(default=None, max_length=255)  # type: ignore


# Todo's database model
class Item(ItemBase, table=True):
	id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
	owner_id: uuid.UUID = Field(
		foreign_key='user.id', nullable=False, ondelete='CASCADE'
	)
	owner: User = Relationship(back_populates='items')


# Todo's public model
class ItemPublic(ItemBase):
	id: uuid.UUID
	owner_id: uuid.UUID


# Todos' public model
class ItemsPublic(SQLModel):
	data: list[ItemPublic]
	count: int


# ----------------------
# Token
# ----------------------
# JSON payload containing access token
class Token(SQLModel):
	access_token: str
	token_type: str = 'bearer'


# Contents of JWT token
class TokenPayload(SQLModel):
	sub: str | None = None
