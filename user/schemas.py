from typing import Optional, List

from pydantic import BaseModel, EmailStr




class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserEmail(BaseModel):
    user_email: EmailStr



class Profile(BaseModel):
    name: str
    number: str
    email: EmailStr
    address: str


    class Config:
        orm_mode = True


class UpdateUser(BaseModel):
    name: Optional[str]
    number: Optional[str]
    # email: EmailStr
    address:Optional [str]

    class Config:
        orm_mode = True


class UpdateUserPassword(BaseModel):
    password: str

    class Config:
        orm_mode = True


