import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

# นำเข้าโมดูลจาก app แพ็กเกจ
from app import crud, models, schemas
from app.database import SessionLocal, engine

# สำหรับ Scalar API reference
from scalar_fastapi import get_scalar_api_reference

# สร้างตารางฐานข้อมูล
models.Base.metadata.create_all(bind=engine)

# สร้างแอปพลิเคชัน FastAPI
app = FastAPI()


# ฟังก์ชันสำหรับรับ session ฐานข้อมูล
def get_db():
    db = SessionLocal()
    try : 
        yield db
    finally:
        db.close()


# เส้นทาง API สำหรับสร้างผู้ใช้ใหม่
# Method: POST
# Path: /users/
@app.post("/users/",response_model=schemas.User)
def post_user(user:schemas.UserCreate, db:Session=Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db,user=user)


# เส้นทาง API สำหรับดึงข้อมูลผู้ใช้ทั้งหมด
# Method: GET
# Path: /users/
@app.get("/users/", response_model=list[schemas.User])
def get_users(skip:int=0, limit:int=0, db:Session=Depends(get_db)):
    users = crud.get_users(db,skip=skip,limit=limit)
    return users


# เส้นทาง API สำหรับดึงข้อมูลผู้ใช้ตาม user_id
# Method: GET
# Path: /users/{user_id}/
@app.get("/users/{user_id}/",response_model=schemas.User)
def get_user(user_id:int, db:Session=Depends(get_db)):
    db_user = crud.get_user(db,user_id =user_id )
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# เส้นทาง API สำหรับสร้าง Todo ใหม่สำหรับผู้ใช้
# Method: POST
# Path: /users/{user_id}/todos/
@app.post("/users/{user_id}/todos/",response_model=schemas.Todo)
def post_todo_for_user(user_id:int, todo:schemas.TodoCreate, db:Session=Depends(get_db)):
    return crud.create_user_todo(db=db,user_id=user_id, todo=todo)


# เส้นทาง API สำหรับดึงข้อมูล Todo ทั้งหมด
# Method: GET
# Path: /todos/
@app.get("/todos/", response_model=list[schemas.Todo])
def get_todos(skip:int=0,limit:int=100,db:Session=Depends(get_db)):
    todos = crud.get_todos(db,skip=skip,limit=limit)
    return todos


# เส้นทาง API สำหรับดู Scalar API reference
# Path: /scalar
@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )


# การรันแอปพลิเคชัน
# ใช้คำสั่งนี้เพื่อรัน: uv run main.py
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)