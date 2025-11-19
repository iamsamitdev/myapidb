from pydantic import BaseModel


# สคีมา Pydantic สำหรับ Todo และ User
# คลาสพื้นฐาน Todo
class TodoBase(BaseModel):
    title : str
    description : str | None = None


# คลาสสำหรับสร้าง Todo
class TodoCreate(TodoBase):
    pass


# คลาส Todo สำหรับแสดงข้อมูล Todo
class Todo(TodoBase):
    id : int
    owner_id  : int

    class Config:
        orm_mode = True


# คลาสพื้นฐาน User
class UserBase(BaseModel):
    email: str
    name: str


# คลาสสำหรับสร้าง User
class UserCreate(UserBase):
    pass 


# คลาส User สำหรับแสดงข้อมูล User
class User(UserBase):
    id : int
    is_active : bool
    todos : list[Todo] = []

    class Config:
        orm_model = True