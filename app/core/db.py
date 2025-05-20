from sqlmodel import create_engine

DATABASE_URL = 'sqlite:///todo_app.db'

engine = create_engine(
	url=DATABASE_URL, echo=True, connect_args={'check_same_thread': False}
)
