from pydantic import BaseModel
from .user_schema import UserBase

class LoginBase(BaseModel):
    id: str
    password: str

class DeleteAccount(LoginBase):
    is_active: bool

class Signup(LoginBase,UserBase):
    pass

class Login(LoginBase):
    is_active: bool

    class Config:
        orm_mode: True