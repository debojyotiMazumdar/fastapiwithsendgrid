from enum import unique
from os import name
from typing import Optional
from pydantic.networks import EmailStr
from sqlalchemy.sql.schema import Table, UniqueConstraint
from sqlmodel import SQLModel
from sqlmodel.main import Field


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: EmailStr
    password: str
    verification_token: str
    is_verified: bool
    session_token: str


class User_Input(SQLModel):
    name: str
    email: EmailStr
    password: str


class User_SignIn_Input(SQLModel):
    email: EmailStr
    password: str
