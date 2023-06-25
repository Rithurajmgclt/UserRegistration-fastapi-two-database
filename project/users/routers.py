
import os
import re
import bcrypt
import base64
from fastapi import APIRouter, UploadFile,File,Form,Depends,Request
from users.schema import UserDetail
from users.models import User
from users.database import SessionLocal, engine
from sqlalchemy import select
from pydantic import ValidationError, EmailStr, constr
from fastapi import Form
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from sqlalchemy.orm import Session
from users.database import get_db
import os
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from users.database import collection as bucket
from starlette.responses import FileResponse

load_dotenv()

user_router = APIRouter()
base_url = os.getenv("base_url")
PASSWORD_REGEX = r"^(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=])[A-Za-z\d@#$%^&+=]{8,}$"




@user_router.get("/users/{user_id}", response_model=UserDetail)
async def get_user(user_id: int, request: Request, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # image_url = f"{base_url}/{user.profile.image_path}"
    image = bucket.find_one({"user": str(user_id)})
    user_detail = UserDetail(
        id=user.id,
        fullname=user.fullname,
        email=user.email,
        phone =user.phone,
        mongo_image_id= str(image["_id"])if image else None)
    return user_detail
@user_router.get("/users/list/", response_model=list[UserDetail])
async def get_user(db: Session = Depends(get_db)):
    users = db.query(User).all()
    if not users:
        raise HTTPException(status_code=404, detail="No users created")
   
    user_list = []
    for user in users:
        image = bucket.find_one({"user": str(user.id)})
        user_with_image = UserDetail(
            id=user.id,
            fullname=user.fullname,
            email=user.email,
            phone=user.phone,
            mongo_image_id= str(image["_id"])if image else None
        )
        user_list.append(user_with_image)

    return user_list


def save_uploaded_file(file: UploadFile, file_path: str):
    with open(file_path, "wb") as buffer:
        while True:
            chunk = file.file.read(1024)
            if not chunk:
                break
            buffer.write(chunk)


@user_router.post("/users/create")
async def create_item(fullname: str = Form(...),
    email: EmailStr = Form(...),
    phone: constr(regex=r'^\+\d{1,3}-\d{3,14}$') = Form(...),
    password: str = Form(...), image: UploadFile = File(...),
    db: Session = Depends(get_db)):
    try:
        # print(password)
        # Create a new User instance\
          #password validation
        if not re.match(PASSWORD_REGEX, password):
            return {'message': 'Password must be at least 8 characters long and contain at least one letter and one digit'}   
          #password hasging
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        new_user = User(
            fullname=fullname,
            email=email,
            phone=phone,
            password=hashed_password,
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        if image and new_user.id:
            image_data = await image.read()
            mongo_data = {"user": str(new_user.id), "image": image_data}
            bucket.insert_one(mongo_data)

        return {"message": "User created successfully", "user_id": new_user.id}

    except (ValidationError, IntegrityError) as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@user_router.get("/users/{user_id}/image")
async def view_image(user_id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(User).get(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        mongo_data = bucket.find_one({"user": str(user_id)})
        if not mongo_data:
            raise HTTPException(status_code=404, detail="Image not found")

        image_data = mongo_data["image"]
        file_path =  f"temp_{user_id}.jpg" 

        with open(file_path, "wb") as file:
            file.write(image_data)

        return FileResponse(file_path, media_type="image/jpeg")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

