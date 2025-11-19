## Python FastAPI with MySQL and ORM with SQLAlchemy

### Technology Stack
- Python
- UV
- FastAPI
- SQLAlchemy
- Alembic
- MySQL

### System Requirements
- Python 3.13.x ขึ้นไป `python --version`
- MySQL Server 8.x ขึ้นไป `mysql --version`
- UV (Universal Virtualenv) `uv --version`

### Step 1: สร้างฐานข้อมูล MySQL
ก่อนอื่นให้สร้างฐานข้อมูล MySQL สำหรับโปรเจ็กต์นี้
```sql
CREATE DATABASE mydb;
```

### Step 2: สร้างโปรเจ็กต์ FastAPI พร้อมฐานข้อมูล MySQL
1. สร้างโฟลเดอร์โปรเจ็กต์ใหม่ด้วย uv
```bash
uv init --python  3.13.5 myapidb

# เปิดเข้า vscode
code myapidb
```

### Step 3: ติดตั้งแพ็กเกจที่จำเป็น
```bash
uv add fastapi sqlalchemy pymysql uvicorn alembic python-dotenv cryptography scalar-fastapi
```
อธิบายแพ็กเกจที่ติดตั้ง:
- fastapi: เว็บเฟรมเวิร์กสำหรับสร้าง API
- sqlalchemy: ORM สำหรับจัดการฐานข้อมูล
- pymysql: ตัวเชื่อมต่อ MySQL สำหรับ Python
- uvicorn: ASGI server สำหรับรันแอป FastAPI
- alembic: เครื่องมือสำหรับจัดการ Migration ของฐานข้อมูล
- python-dotenv: สำหรับโหลดตัวแปรสภาพแวดล้อมจากไฟล์ .env
- cryptography: สำหรับการเข้ารหัสและความปลอดภัย
- scalar-fastapi: แพ็กเกจเสริมสำหรับดู API reference ในรูปแบบ HTML

### Step 4: สร้าง migration เบื้องต้นด้วย Alembic
```bash
uv run alembic init migrations
```

### Step 5: สร้างไฟล์ .env สำหรับเก็บการตั้งค่าฐานข้อมูล
สร้างไฟล์ `.env` ในโฟลเดอร์โปรเจ็กต์ และเพิ่มการตั้งค่าดังนี้:
```
DB_URL=mysql+pymysql://username:password@localhost:3306/mydb
```

### Step 6: สร้างไฟล์ `database.py` สำหรับการเชื่อมต่อฐานข้อมูลในโฟลเดอร์ app
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# ดึงค่าตัวแปรสภาพแวดล้อมจากไฟล์ .env
load_dotenv()
import os

DB_URL = os.getenv("DB_URL")
engine = create_engine(DB_URL,echo=True)
SessionLocal = sessionmaker(autocommit=False,autoflush=False, bind=engine)

Base = declarative_base()
```

### Step 7: สร้างไฟล์ `models.py` สำหรับสร้างโมเดลฐานข้อมูลในโฟลเดอร์ app
```python
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
```

### Step 8: สร้างไฟล์ `schemas.py` สำหรับสร้าง Pydantic models ในโฟลเดอร์ app
```python
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
```

### Step 9: สร้างไฟล์ `crud.py` สำหรับฟังก์ชัน CRUD ในโฟลเดอร์ app
```python
from sqlalchemy.orm import Session
from app import models,schemas

# ฟังก์ชัน CRUD สำหรับ User และ Todo
# ดึงข้อมูลผู้ใช้ตาม user_id
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# ดึงข้อมูลผู้ใช้ตาม email
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# ดึงข้อมูลผู้ใช้ทั้งหมด โดยมีการข้าม (skip) และจำกัดจำนวน (limit)
def get_users(db: Session, skip:int=0, limit:int=100):
    # return db.query(models.User).offset(skip).limit(limit).all()
    return db.query(models.User).offset(skip).limit(limit).all()

# สร้างผู้ใช้ใหม่
def create_user(db: Session, user:schemas.UserCreate):
    db_user = models.User(email=user.email,
                          name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# ดึงข้อมูล Todo ทั้งหมด โดยมีการข้าม (skip) และจำกัดจำนวน (limit)
def get_todos(db: Session, skip:int=0, limit: int=100):
    return db.query(models.Todo).offset(skip).limit(limit).all()

# สร้าง Todo ใหม่สำหรับผู้ใช้
def create_user_todo(db:Session, todo:schemas.TodoCreate, user_id : int):
    db_todo = models.Todo(**todo.model_dump(),owner_id=user_id )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo
```

### Step 10: แก้ไขไฟล์ `migrations/env.py` เพื่อเชื่อมต่อฐานข้อมูล
```python
from logging.config import fileConfig
import os

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from  alembic import context

# เพิ่มโค้ด
from app.models import Base
target_metadata = Base.metadata

import sys
sys.path.append(os.getcwd())

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
# เพิ่มโค้ด
from app.database import DB_URL
config = context.config
config.set_main_option('sqlalchemy.url',DB_URL) #os.getenv('DB_URI'))

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
# target_metadata = None

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### Step 11: สร้างไฟล์ Migration ใหม่
สั่งให้ Alembic สร้างไฟล์ Migration ใหม่ตามโครงสร้างปัจจุบันของโมเดล
```bash
uv run alembic revision --autogenerate -m "Initial migration"
```
> จะมีการสร้างไฟล์ migration ใหม่ในโฟลเดอร์ `migrations/versions/`

### Step 12: ใช้ Migration เพื่อสร้างตารางในฐานข้อมูล
```bash
uv run alembic upgrade head
```

### Step 13: แก้ไขไฟล์ `main.py` เพื่อสร้างเส้นทาง API
```python
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
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
```

## Step 14: รันแอปพลิเคชัน
ใช้คำสั่งต่อไปนี้เพื่อรันแอปพลิเคชัน FastAPI
```bash
uv run main.py
```

### Step 15: ทดสอบ API
เปิดเว็บเบราว์เซอร์และไปที่ URL ต่อไปนี้เพื่อตรวจสอบ API:
- เอกสาร API อัตโนมัติ: `http://localhost:8000/docs`
- Scalar API reference: `http://localhost:8000/scalar`

### API Endpoints Summary
- สร้างผู้ใช้ใหม่: `POST /users/`
- ดึงข้อมูลผู้ใช้ทั้งหมด: `GET /users/`
- ดึงข้อมูลผู้ใช้ตาม user_id: `GET /users/{user_id}/`
- สร้าง Todo ใหม่สำหรับผู้ใช้: `POST /users/{user_id}/todos/`
- ดึงข้อมูล Todo ทั้งหมด: `GET /todos/`

---
### Troubleshooting

หากคุณต้องการเริ่มต้นระบบ Migration ใหม่ทั้งหมด (Reset Migration) เพื่อให้เหมือนกับเพิ่งเริ่มโปรเจ็กต์ สามารถทำตามขั้นตอนที่ผมเพิ่งทำให้ได้เลย

1. ล้างข้อมูลใน Database (Downgrade): สั่งให้ Alembic ย้อนกลับการเปลี่ยนแปลงทั้งหมดเพื่อลบตารางเก่าออก
```bash
uv run alembic downgrade base
```

2. ลบไฟล์ Migration เก่า: ลบไฟล์ `.py` ในโฟลเดอร์ `versions` ทิ้งให้หมด
```bash
# Windows PowerShell
Remove-Item migrations\versions\*.py

# CMD
del migrations\versions\*.py

# Linux / macOS
rm -rf migrations/versions/*.py
```

3. สร้างไฟล์ Migration ใหม่: สั่งให้ Alembic สร้างไฟล์ Migration ใหม่ตามโครงสร้างปัจจุบันของโมเดล
```bash
uv run alembic revision --autogenerate -m "Initial migration"
```

4. อัพเดต Database: สั่งให้ Alembic อัพเดตฐานข้อมูลตามไฟล์ Migration ใหม่
```bash
uv run alembic upgrade head
```

---
### คำสั่งน่าสนใจเพิ่มเติม
- ซิงค์แพ็กเกจใน uvenv กับไฟล์ `uv.lock`:
```bash
uv sync
```
- ดูรายการ package ที่ติดตั้งใน uvenv:
```bash
uv pip list
```
- ติดตั้ง package เพิ่มเติมใน uvenv:
```bash
uv add package_name
```
- ถอนการติดตั้ง package ใน uvenv:
```bash
uv remove package_name
```
- freeze รายการ package ที่ติดตั้งใน uvenv ลงในไฟล์ `requirements.txt`:
```bash
uv pip freeze > requirements.txt
```
- ติดตั้ง package จากไฟล์ `requirements.txt` ลงใน uvenv:
```bash
uv pip install -r requirements.txt

หรือ

uv add -r requirements.txt
```

## การใช้งาน Docker Container กับโปรเจ็กต์นี้
คุณสามารถใช้ Docker เพื่อรันฐานข้อมูล MySQL และแอปพลิเคชัน FastAPI ได้อย่างง่ายดาย โดยใช้ไฟล์ `Dockerfile`  และ `docker-compose.yml`

### Step 1: แก้ไขไฟล์ `.env` 
สำหรับเก็บตัวแปรสภาพแวดล้อม
```env
DB_URL="mysql+pymysql://username:password@localhost:3306/mydb"
MYSQL_ROOT_PASSWORD=yourpassword
MYSQL_DATABASE=mydb
MYSQL_USER=root
MYSQL_PORT=3307
```

MYSQL_ROOT_PASSWORD=yourpassword

### Step 2: สร้างไฟล์ `Dockerfile` 
สำหรับแอปพลิเคชัน FastAPI
```Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Install uv
RUN pip install uv

# Copy the project configuration files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
# --frozen ensures we use the exact versions from uv.lock
RUN uv sync --frozen

# Copy the rest of the application code
COPY . .

# Add the virtual environment to the PATH
ENV PATH="/app/.venv/bin:$PATH"

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Step 3: สร้างไฟล์ `docker-compose.yml` 
สำหรับรัน MySQL และแอปพลิเคชัน FastAPI
```yaml
networks:
  myapidb-network:
    name: myapidb-network
    driver: bridge

services:
  db:
    image: mysql:8.0
    container_name: myapidb-mysql
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: "${MYSQL_ROOT_PASSWORD}"
      MYSQL_DATABASE: "${MYSQL_DATABASE}"
    ports:
      - "${MYSQL_PORT}:3306" # Map host port to container port 3306
    volumes:
      - db_data:/var/lib/mysql
    networks:
      - myapidb-network
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-u", "root", "-p${MYSQL_ROOT_PASSWORD}"]
      interval: 10s
      timeout: 5s
      retries: 5

  web:
    build: .
    container_name: myapidb-web
    restart: always
    ports:
      - "8000:8000"
    environment:
      # Use the service name 'db' as the hostname
      DB_URL: "mysql+pymysql://${MYSQL_USER}:${MYSQL_ROOT_PASSWORD}@db:3306/${MYSQL_DATABASE}"
    depends_on:
      db:
        condition: service_healthy
    networks: 
      - myapidb-network
    # Optional: Run migrations automatically on startup
    command: sh -c "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000"

volumes:
  db_data:
```

### Step 4: สร้างไฟล์ `.dockerignore` 
เพื่อไม่ให้ไฟล์ที่ไม่จำเป็นถูกคัดลอกไปยังอิมเมจ Docker
```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/
pip-log.txt
pip-delete-this-directory.txt
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.log
.git
.mypy_cache
.pytest_cache
.hypothesize
.env
.vscode/
.idea/
```

### Step 5: รัน Docker Compose
ใช้คำสั่งต่อไปนี้เพื่อสร้างและรันคอนเทนเนอร์
```bash
docker compose up -d --build
```

### Step 6: ทดสอบ API
เปิดเว็บเบราว์เซอร์และไปที่ URL ต่อไปนี้เพื่อตรวจสอบ API:
- เอกสาร API อัตโนมัติ: `http://localhost:8000/docs`
- Scalar API reference: `http://localhost:8000/scalar`

### API Endpoints Summary
- สร้างผู้ใช้ใหม่: `POST /users/`
- ดึงข้อมูลผู้ใช้ทั้งหมด: `GET /users/`
- ดึงข้อมูลผู้ใช้ตาม user_id: `GET /users/{user_id}/`
- สร้าง Todo ใหม่สำหรับผู้ใช้: `POST /users/{user_id}/todos/`
- ดึงข้อมูล Todo ทั้งหมด: `GET /todos/`

### คำสั่งเพิ่มเติมสำหรับจัดการคอนเทนเนอร์ Docker:

- หากต้องการหยุดคอนเทนเนอร์:
```bash
docker compose stop
```

- หากต้องการลบคอนเทนเนอร์และเครือข่ายที่สร้างขึ้น:
```bash
docker compose down

# หรือลบพร้อมกับข้อมูลในโวลุ่ม: (ระวังข้อมูลจะหายหมด)
docker compose down -v

# หรือลบทั้งอิมเมจด้วย: (ระวังข้อมูลจะหายหมด)
docker compose down --rmi all -v
```

- หากต้องการดูบันทึกของคอนเทนเนอร์:
```bash
docker compose logs -f
```

- หากต้องการเข้าสู่เชลล์ของคอนเทนเนอร์แอปพลิเคชัน:
```bash
docker exec -it myapidb-web /bin/sh
```

- หากต้องการเข้าสู่เชลล์ของคอนเทนเนอร์ฐานข้อมูล:
```bash
docker exec -it myapidb-mysql /bin/sh
```




