from contextlib import asynccontextmanager

from fastapi import FastAPI
from rich import panel, print
from scalar_fastapi import get_scalar_api_reference
from sqlmodel import SQLModel

from app import models  # noqa: F401
from app.api.main import api_router
from app.core.db import engine


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001
	print(panel.Panel('Tables are created'))
	SQLModel.metadata.create_all(engine)
	yield
	print(panel.Panel('Tables are removed'))
	SQLModel.metadata.drop_all(engine)


app = FastAPI(lifespan=lifespan)


@app.get('/')
def hello_world():
	return {'message': 'hello world'}


@app.get('/scalar', include_in_schema=False)
def get_scalar_docs():
	return get_scalar_api_reference(
		openapi_url=app.openapi_url,  # type: ignore
		title='Scalar Documentation API',
	)


# @app.on_event(event_type='startup')
# def on_startup():


app.include_router(api_router)
