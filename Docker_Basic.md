## พื้นฐานการใช้งาน Docker

## โปรแกรม (Tool and Editor) ที่ใช้อบรม
1. **Docker Desktop**

---

## การตรวจสอบความเรียบร้อยของเครื่องมือที่ติดตั้งบน Windows / Mac OS / Linux

เปิด Command Prompt บน Windows หรือ Terminal บน Mac ขึ้นมาป้อนคำสั่งดังนี้


### Docker
```bash
docker --version
docker compose version
docker info
```

---

## พื้นฐานการใช้งาน Docker

- การติดตั้ง Docker Desktop
- การใช้งานคำสั่งพื้นฐานของ Docker
- การสร้างและจัดการ Container
- การสร้าง Dockerfile และ Docker Image
- การใช้งาน Docker Compose

#### 1. การติดตั้ง Docker Desktop
- ดาวน์โหลดและติดตั้ง Docker Desktop จาก [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
- ตรวจสอบการติดตั้งโดยรันคำสั่ง:
```bash
docker --version
docker compose version
docker info
```

#### 2. การใช้งานคำสั่งพื้นฐานของ Docker
##### 2.1 รัน hello-world container
```bash
docker run hello-world
```
> คำสั่งนี้จะดาวน์โหลดและรัน container ที่แสดงข้อความต้อนรับจาก Docker

##### 2.2 ดูรายการ container ที่กำลังรันอยู่
```bash
docker ps
docker ps -a  # ดู container ทั้งหมดรวมถึงที่หยุดแล้ว
```

##### 2.3 หยุด container
```bash
docker stop <container_id>
```

##### 2.4 ลบ container
```bash
docker rm <container_id>
```

##### 2.5 ดูรายการ image ที่มีอยู่
```bash
docker images
docker image ls
```
##### 2.6 ลบ image
```bash
docker rmi <image_id>
```

#### 3. การสร้างและจัดการ Container
##### 3.1 รัน container จาก image
```bash
docker run -d -p 8880:80 --name mynginx nginx
```
> คำสั่งนี้จะรัน Nginx container ในโหมด detached และแมปพอร์ต 80 ของ container ไปยังพอร์ต 8880 ของโฮสต์

##### 3.2 เข้าสู่ shell ของ container
```bash
docker exec -it mynginx /bin/bash
# หรือ
docker exec -it mynginx /bin/sh
```

##### 3.3 ดู log ของ container
```bash
docker logs mynginx
```

#### 4. การสร้าง Dockerfile และ Docker Image

##### 4.1 สร้างโฟลเดอร์โปรเจ็กต์
```bash
mkdir basic-docker/docker-node-app
cd basic-docker/docker-node-app
```

##### 4.2 สร้างไฟล์ package.json
```bash
npm init -y
```

##### 4.3 กำหนดสคริปต์ใน package.json
```json
{
  "name": "docker-node-app",
  "version": "1.0.0",
  "description": "A simple Node.js app for Docker",
  "main": "index.js",
  "scripts": {
    "dev": "nodemon index.js",
    "start": "node index.js"
  },
  "author": "Your Name",
  "license": "ISC",
  "dependencies": {
    "express": "^4.18.2",
    "nodemon": "^2.0.22"
  }
}
```
> nodemon เป็นเครื่องมือที่ช่วยในการพัฒนา Node.js โดยจะทำการรีสตาร์ทเซิร์ฟเวอร์อัตโนมัติเมื่อมีการเปลี่ยนแปลงในโค้ด

##### 4.4 สร้างไฟล์ index.js
```javascript
const express = require('express')
const app = express()

// ทำ url ให้สามารถเข้าถึงได้
app.get('/', (req, res) => {
  res.send('Hello World!')
})

// run the server
app.listen(3000, () => {
  console.log('Server is running on http://localhost:3000')
})
```

##### 4.5 สร้างไฟล์ Dockerfile

> ไฟล์ Dockerfile เป็นไฟล์ข้อความธรรมดาที่ใช้กำหนดขั้นตอนการสร้าง Docker Image โดยระบุฐานของ image, การติดตั้ง dependencies, การคัดลอกไฟล์, การตั้งค่าพอร์ต และคำสั่งที่ต้องรันเมื่อ container เริ่มทำงาน

```Dockerfile
# โหลด image ของ node จาก docker hub
FROM node:alpine

# กำหนด directory ที่จะใช้เก็บไฟล์ของโปรเจค
WORKDIR /app

# คัดลอกไฟล์ package.json และ package-lock.json ไปยัง directory ที่กำหนดไว้
COPY package*.json ./

# ติดตั้ง package ที่ระบุในไฟล์ package.json
RUN npm install

# ติดตั้ง nodemon เพื่อใช้ในการรันโปรเจค
RUN npm install -g nodemon

# คัดลอกไฟล์ทั้งหมดไปยัง directory ที่กำหนดไว้
COPY . .

# ระบุ port ที่จะใช้
EXPOSE 3000

# รันคำสั่ง npm run dev เมื่อ container ถูกสร้างขึ้น
CMD ["npm", "run", "dev"]
```

##### 4.6 สร้าง Docker Image
```bash
docker build -t docker-node-app .
```

##### 4.7 รัน Docker Container
```bash
docker run -d -p 3300:3000 --name mydockerapp docker-node-app
```

#### 5. การใช้งาน Docker Compose
##### 5.1 สร้างไฟล์ docker-compose.yml
```yaml
networks:
  nodejs_network:
    name: nodejs_network
    driver: bridge

services:

  # NodeJS App
  nodejs:
    build:
      context: .
      dockerfile: Dockerfile
    image: mynodeapp:1.0
    container_name: mynodeapp
    volumes:
      - .:/app
      - /app/node_modules
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
      - CHOKIDAR_USEPOLLING=true # สำหรับ Windows เพื่อให้ nodemon ทำงานได้
    networks:
      - nodejs_network
    restart: always

  # MongoDB
  mongodb:
    image: mongo
    container_name: mongodb
    ports:
      - "28017:27017"
    networks:
      - nodejs_network
    restart: always
    volumes:
      - mongo_data:/data/db

volumes:
  mongo_data:
    name: mongo_data
    driver: local
```

##### 5.2 รัน Docker Compose
```bash
# เช็คความถูกต้องของไฟล์ docker-compose.yml
docker compose config

# รัน Docker Compose
docker compose up -d

# หรือถ้ามีการเปลี่ยนแปลงไฟล์ Dockerfile หรือ docker-compose.yml
docker compose up -d --build
```

##### 5.3 ตรวจสอบสถานะของ Container
```bash
docker compose ps
```

##### 5.4 หยุดและลบ Container
```bash
docker compose down

# หรือถ้าต้องการลบข้อมูลทั้งหมดรวมถึง volume
docker compose down -v

# หรือถ้าต้องการลบ image ด้วย
docker compose down --rmi all -v
```

#### 6. DockerHub (การใช้งาน Docker Hub)
##### 6.1 สร้างบัญชีผู้ใช้บน Docker Hub
- ไปที่ [Docker Hub](https://hub.docker.com/) และสมัครสมาชิก
- สร้าง Repository ใหม่บน Docker Hub
  - คลิกที่ปุ่ม "Create Repository"
  - กรอกชื่อ Repository เช่น `mynodeapp`
  - เลือก Public หรือ Private ตามต้องการ
  - คลิกที่ปุ่ม "Create"

> สำหรับการใช้งาน Docker Hub แนะนำให้ใช้บัญชีแบบ Public เพราะจะง่ายต่อการเข้าถึงและใช้งานร่วมกับผู้อื่น
> เวอ์ร์ชันฟรีของ Docker Hub มีข้อจำกัดในการสร้าง Repository แบบ Private และมีข้อจำกัดในการดึง (pull) image จาก Repository ในระยะเวลาหนึ่ง

##### 6.2 เข้าสู่ระบบ Docker Hub ผ่าน Command Line
```bash
docker login
```

##### 6.3 การ Tag Image และ Push ขึ้น Docker Hub

| คำสั่ง | คำอธิบาย |
|--------|-----------|
| `docker tag <image>:<old_tag> <username>/<repo>:<new_tag>` | สร้างแท็กใหม่ให้ image เพื่อเตรียม push |


```bash
docker tag mynodeapp:1.0 <your-dockerhub-username>/mynodeapp:1.0
```

##### 6.4 ดัน (Push) Docker Image ไปยัง Docker Hub

| คำสั่ง | คำอธิบาย |
|--------|-----------|
| `docker push <username>/<repo>:<tag>` | อัปโหลด image พร้อมแท็กขึ้น Docker Hub |

```bash
docker push <your-dockerhub-username>/mynodeapp:1.0
```

##### 6.5 ดึง (Pull) Docker Image จาก Docker Hub

| คำสั่ง | คำอธิบาย |
|--------|-----------|
| `docker pull <username>/<repo>:<tag>` | ดาวน์โหลด image จาก Docker Hub |

```bash
docker pull <your-dockerhub-username>/mynodeapp:1.0
```