import os
from dotenv import load_dotenv
from sqlalchemy import sql
from sqlmodel import create_engine, Session, SQLModel
import sqlmodel
from typing import Optional
from sqlmodel.main import Field

load_dotenv()

database_url = os.getenv("database_url")

engine = create_engine(database_url, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
