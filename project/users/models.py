from sqlalchemy import Column, Integer, String,ForeignKey
from users.database import Base
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String,unique=True, index=True)
    password = Column(String)
    profile = relationship("Profile", uselist=False, back_populates="user")

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    image_path = Column(String)

    # Relationship with the User table
    user = relationship("User", back_populates="profile")    
