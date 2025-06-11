from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference
from sqlmodel import SQLModel

from app import models  # noqa: F401
from app.api.main import api_router
from app.core.db import engine

app = FastAPI()


@app.get('/')
def hello_world():
	return {'message': 'hello world'}


@app.get('/scalar', include_in_schema=False)
def get_scalar_docs():
	return get_scalar_api_reference(
		openapi_url=app.openapi_url,  # type: ignore
		title='Scalar Documentation API',
	)


@app.on_event(event_type='startup')
def on_startup():
	SQLModel.metadata.drop_all(engine)
	SQLModel.metadata.create_all(engine)


app.include_router(api_router)
