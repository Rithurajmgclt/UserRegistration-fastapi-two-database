from pydantic import BaseModel
from pydantic import ValidationError, EmailStr, constr
from fastapi import Form
from typing import Optional
class Usercreate(BaseModel):
    fullname: str
    phone: constr(regex=r'^\+\d{1,3}-\d{3,14}$')
    email:EmailStr
    password:  str

class UserDetail(BaseModel):
    id: int
    fullname: str
    email: str
    phone:str
    mongo_image_id: Optional[str] = None

