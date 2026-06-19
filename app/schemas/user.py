from pydantic import BaseModel
from pydantic import EmailStr
from typing import Literal


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Literal[
        "client",
        "lawyer",
        "admin"
    ]


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True