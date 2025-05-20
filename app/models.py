import uuid

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


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
class UsersPublic(UserBase):
	data: list[UserPublic]
	count: int


class Item(SQLModel, table=True):
	pass
