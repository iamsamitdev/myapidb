## พื้นฐานการใช้งาน Kubernetes

### โปรแกรม (Tool and Editor) ที่ใช้อบรม
1. **Docker Desktop**
2. **Kind**
3. **Lens IDE**

---

### การตรวจสอบความเรียบร้อยของเครื่องมือที่ติดตั้งบน Windows / Mac OS / Linux

เปิด Command Prompt บน Windows หรือ Terminal บน Mac ขึ้นมาป้อนคำสั่งดังนี้

### Docker
```bash
docker --version
docker compose version
docker info
```

### kubectl
```bash
kubectl version --client
kubectl cluster-info
```

### kind
```bash
kind --version
```

---

### การติดตั้ง Docker Desktop
- ดาวน์โหลดและติดตั้ง Docker Desktop จาก [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
- เปิดโปรแกรม Docker Desktop ขึ้นมา
- ตรวจสอบสถานะการทำงานของ Docker Desktop ว่าแสดงว่า "Docker is running" หรือไม่
- ตั้งค่าให้ Docker Desktop ใช้งาน Kubernetes โดยไปที่ "Settings" > "Kubernetes" แล้วติ๊กเลือก "Enable Kubernetes" จากนั้นกด "Apply & Restart"
- รอจนกว่า Kubernetes จะถูกติดตั้งและพร้อมใช้งาน
- ตรวจสอบการติดตั้ง Kubernetes โดยใช้คำสั่ง `kubectl cluster-info` ใน Command Prompt หรือ Terminal

---

### การติดตั้ง kind
- ติดตั้ง kind โดยใช้คำสั่งดังนี้
```bash
# สำหรับ Windows (ใช้ PowerShell)
curl -Lo ./kind-windows-amd64.exe https://kind.sigs.k8s.io/dl/v0.11.1/kind-windows-amd64
move ./kind-windows-amd64.exe /usr/local/bin/kind.exe

# สำหรับ Mac OS
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.11.1/kind-darwin-amd64
chmod +x ./kind
mv ./kind /usr/local/bin/kind

# สำหรับ Linux
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.11.1/kind-linux-amd64
chmod +x ./kind
mv ./kind /usr/local/bin/kind
```

- ตรวจสอบการติดตั้ง kind โดยใช้คำสั่ง
```bash
kind --version
```
--- 

### การสร้างคลัสเตอร์ Kubernetes ด้วย kind
1. สร้างไฟล์คอนฟิกูเรชันสำหรับคลัสเตอร์
```yaml
# 00-kind-create-cluster.yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
- role: worker
- role: worker
- role: worker
```
2. สร้างคลัสเตอร์ Kubernetes โดยใช้คำสั่ง
```bash
kind create cluster --name my-cluster --config 00-kind-create-cluster.yaml
```

3. ตรวจสอบสถานะของคลัสเตอร์ที่สร้างขึ้น
```bashbash
kubectl cluster-info --context kind-my-cluster
kubectl get nodes
```

4. ลบคลัสเตอร์ Kubernetes ที่สร้างขึ้น (ถ้าต้องการ)
```bash
kind delete cluster --name my-cluster
```

---

### การติดตั้ง Lens IDE
- ดาวน์โหลดและติดตั้ง Lens IDE จาก [https://k8slens.dev/](https://k8slens.dev/)
- เปิดโปรแกรม Lens IDE ขึ้นมา
- เพิ่มคลัสเตอร์ Kubernetes ที่สร้างด้วย kind โดยเลือก "Add Cluster" และเลือก "kind" จากนั้นเลือกคลัสเตอร์ที่ต้องการเชื่อมต่อ
- ตรวจสอบการเชื่อมต่อคลัสเตอร์โดยดูที่สถานะของคลัสเตอร์ใน Lens IDE ว่าแสดงว่า "Connected" หรือไม่
- เรียนรู้การใช้งาน Lens IDE เบื้องต้น เช่น การดู Pods, Deployments, Services และการจัดการทรัพยากรต่างๆ ในคลัสเตอร์ Kubernetes ผ่าน Lens IDE
---

### Kubernetes Resources
- Pods
- Deployments
- Services
- ConfigMaps
- Secrets
- Namespaces
- Persistent Volumes (PVs) and Persistent Volume Claims (PVCs)

### Kubernetes Architecture
- Master Node
- Worker Nodes
- kube-apiserver
- etcd
- kube-scheduler
- kube-controller-manager
- kubelet
- kube-proxy
- Container Runtime (e.g., Docker, containerd)

### คำสั่งพื้นฐานเพื่อดูข้อมูล Cluster

1. `kubectl version` (ดูเวอร์ชันของ kubectl และ Kubernetes cluster)
2. `kubectl config view` (ดูข้อมูลไฟล์ config ของ k8s)
3. `kubectl config get-contexts` (ดูรายชื่อ cluster ทั้งหมด)
4. `kubectl config current-context` (ดูว่าปัจจุบันทำงานกับ cluster ไหน)
5. `kubectl config use-context docker-desktop` (สลับ cluster)
6. `kubectl cluster-info` (ดูข้อมูล cluster)
7. `kubectl get nodes` (ดูรายชื่อ node ใน cluster)
8. `kubectl get all --all-namespaces` (ดูทรัพยากรทั้งหมดในทุก namespace)
9. `kubectl get pods --all-namespaces` (ดูรายชื่อ pod ทั้งหมดในทุก namespace)
10. `kubectl get namespaces` or `kubectl get ns` (ดูรายชื่อ namespace ทั้งหมด)
11. `kubectl get svc --all-namespaces` (ดูรายชื่อ service ทั้งหมดในทุก namespace)
12. `kubectl get deployments --all-namespaces` (ดูรายชื่อ deployment ทั้งหมดในทุก namespace)
13. `kubectl get replicaset --all-namespaces` (ดูรายชื่อ replicaset ทั้งหมดในทุก namespace)
14. `kubectl get events --all-namespaces` (ดูรายชื่อ event ทั้งหมดในทุก namespace)
15. `kubectl describe node [node-name]` (ดูรายละเอียด node)
16. `kubectl describe pod [pod-name] -n [namespace]` (ดูรายละเอียด pod ใน namespace ที่ระบุ)
17. `kubectl describe svc [service-name] -n [namespace]` (ดูรายละเอียด service ใน namespace ที่ระบุ)
18. `kubectl describe deployment [deployment-name] -n [namespace]` (ดูรายละเอียด deployment ใน namespace ที่ระบุ)
19. `kubectl logs [pod-name] -n [namespace]` (ดู logs ของ pod ใน namespace ที่ระบุ)
20. `kubectl exec -it [pod-name] -n [namespace] -- /bin/bash` (เข้าสู่ shell ของ pod ใน namespace ที่ระบุ)

---

### การสร้าง Namespace ใหม่
```bash
kubectl create namespace demok8s
```

### การตั้งค่า Context ให้ใช้งานกับ Namespace ที่สร้างขึ้น
```bash
kubectl config set-context --current --namespace=demok8s
```
---

### การสร้าง Pod ง่ายๆ ด้วยไฟล์ YAML
1. สร้างไฟล์คอนฟิกูเรชันสำหรับ Pod `01-pod.yaml`
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: linux
  namespace: demok8s
spec:
  containers:
    - name: busybox
      image: busybox
      command:
        - sleep
        - "3600" # sleep for 1 hour
      resources:
        requests:
          memory: "64Mi" # 64 Mebibytes = 67108864 bytes
          cpu: "250m" # 250 millicpu = 0.25 cpu
        limits:
          memory: "128Mi" # 128 Mebibytes = 134217728 bytes
          cpu: "500m" # 500 millicpu = 0.5 cpu
    - name: alpine
      image: alpine
      command:
        - sleep
        - "3600" # sleep for 1 hour
      resources:
        requests:
          memory: "64Mi"
          cpu: "250m"
        limits:
          memory: "128Mi"
          cpu: "500m"
```

2. สร้าง Pod โดยใช้คำสั่ง
```bash
kubectl apply -f 01-pod.yaml
```

3. ตรวจสอบสถานะของ Pod ที่สร้างขึ้น
```bash
kubectl get pods
```
---

### การสร้าง Deployment ง่ายๆ ด้วยไฟล์ YAML
1. สร้างไฟล์คอนฟิกูเรชันสำหรับ Deployment `02-deployment.yaml`
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
  labels:
    app: nginx
  namespace: demok8s
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: nginx
          resources:
            requests:
              memory: "64Mi"
              cpu: "250m"
            limits:
              memory: "128Mi"
              cpu: "500m"
```
2. สร้าง Deployment โดยใช้คำสั่ง
```bash
kubectl apply -f 02-deployment.yaml
```

3. ตรวจสอบสถานะของ Deployment ที่สร้างขึ้น
```bash
kubectl get deployments
```

---

### การสร้าง Service ง่ายๆ ด้วยไฟล์ YAML
1. สร้างไฟล์คอนฟิกูเรชันสำหรับ Service `03-service.yaml`
```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx
  namespace: demok8s
spec:
  type: NodePort # ClusterIP,  NodePort, LoadBalancer, ExternalName
  #type: LoadBalancer
  ports:
    - targetPort: 80 #  container port nginx run is 80
      port: 8800 # service port ข้างนอกเข้ามา expose ที่ port 8800
      nodePort: 30080 # ถ้าเป็น NodePort จะเป็น port ที่เราจะเข้ามาใช้งาน
      protocol: TCP
  selector:
    app: nginx
```
2. สร้าง Service โดยใช้คำสั่ง
```bash
kubectl apply -f 03-service.yaml
```

3. ตรวจสอบสถานะของ Service ที่สร้างขึ้น
```bash
kubectl get services
```

---

### การทำ Rolling Update Deployment
1. แก้ไขไฟล์คอนฟิกูเรชันสำหรับ Deployment `04-rolling-update.yaml` เปลี่ยน image เป็นเวอร์ชันใหม่
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
  labels:
    app: nginx
  namespace: demok8s
spec:
  replicas: 4
  selector:
    matchLabels:
      app: nginx
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 2 # จำนวน pod ที่จะสร้างขึ้นมาเพิ่มเมื่อมีการ update
      maxUnavailable: 1 # จำนวน pod ที่จะถูกลบออกไปเมื่อมีการ update
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: httpd
          image: httpd
          resources:
            requests:
              memory: "100Mi"
              cpu: "100m"
            limits:
              memory: "200Mi"
              cpu: "200m"
```

2. อัพเดต Deployment โดยใช้คำสั่ง
```bash
kubectl apply -f 04-rolling-update.yaml
```

3. ตรวจสอบสถานะของ Deployment ที่อัพเดต
```bash
kubectl get deployments
```
