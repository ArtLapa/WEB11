# schemas.py

from pydantic import BaseModel
from typing import Optional
from datetime import date

# Класи схем

class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birthday: date
    additional_info: Optional[str] = None

class ContactCreate(ContactBase):
    pass

class ContactUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    birthday: Optional[date] = None
    additional_info: Optional[str] = None

    class Config:
        orm_mode = True

class Contact(ContactBase):
    id: int

    class Config:
        orm_mode = True

class User(BaseModel):
    username: str

    class Config:
        orm_mode = True
