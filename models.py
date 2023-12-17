from database import Base
from sqlalchemy import Column, Integer, String, Boolean

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    phone = Column(Integer)
    profile_pic = Column(Boolean)