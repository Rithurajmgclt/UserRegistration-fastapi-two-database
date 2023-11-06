from sqlalchemy import Column, Integer, String,ForeignKey
from sqlalchemy.orm import relationship

from users.database import Base

class User(Base):
    """
    Table to save user details
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String,unique=True, index=True)
    password = Column(String)
    profile = relationship("Profile", uselist=False, back_populates="user")

class Profile(Base):
    """
    table to save pofile details
    """
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    image_path = Column(String)

    user = relationship("User", back_populates="profile")    
