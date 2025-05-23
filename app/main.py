from fastapi import FastAPI
from sqlmodel import SQLModel

from app import models  # noqa: F401
from app.api.main import api_router
from app.core.db import engine

app = FastAPI()


@app.get('/')
def hello_world():
	return {'message': 'hello world'}


@app.on_event(event_type='startup')
def on_startup():
	SQLModel.metadata.drop_all(engine)
	SQLModel.metadata.create_all(engine)


app.include_router(api_router)
