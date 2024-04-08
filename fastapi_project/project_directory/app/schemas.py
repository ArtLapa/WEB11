# schemas.py

from pydantic import BaseModel

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

class UserInDB(User):
    hashed_password: str


class ContactBase(BaseModel):
    name: str
    email: str
    phone_number: str

class ContactCreate(ContactBase):
    pass

class Contact(ContactBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
