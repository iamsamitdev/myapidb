from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

# สร้างโมเดลฐานข้อมูลโดยใช้ SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


# คลาสโมเดล User และ Todo
# คลาส User สำหรับตาราง users
class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(255),index=True)
    email = Column(String(255), unique=True, index=True)
    todos = relationship("Todo",back_populates="owner")
    is_active = Column(Boolean,default=False)


# คลาส Todo สำหรับตาราง todos
class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    description = Column(String(255), index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User",back_populates="todos")