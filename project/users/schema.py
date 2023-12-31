from pydantic import BaseModel
from pydantic import validator, EmailStr
from typing import Optional
import re



class Usercreate(BaseModel):
    """
    this classs is for user create

    """
    fullname: str
    phone: str
    email:EmailStr
    password:  str
    @validator('phone')
    def validate_phone(cls, value):
        pattern = r'^\+\d{1,3}-\d{3,14}$'
        if not re.match(pattern, value):
            raise ValueError('Invalid phone number format. It should be in the format "+[country code]-[area code]-[phone number]"')
        return value

class UserDetail(BaseModel):
    """
    this class is for getting user details
    """
    id: int
    fullname: str
    email: str
    phone:str
    mongo_image_id: Optional[str] = None

