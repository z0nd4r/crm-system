from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class UserReg(BaseModel):
    model_config = ConfigDict(strict = True)

    username: str
    password: str
    email: EmailStr 
    active: bool = True


class UserAuth(BaseModel):
    model_config = ConfigDict(strict = True)

    email: EmailStr 
    password: str


class UserMain(BaseModel):
    id: int
    username: str
    email: EmailStr 
    active: bool = True

    class Config:
        from_attributes = True