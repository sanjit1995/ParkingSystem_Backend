from datetime import date
from typing import List, Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str
    address: str
    dob: date
    contact_number: int
    gender: str


class User(UserBase):
    user_id: str

    class Config:
        orm_mode = True
