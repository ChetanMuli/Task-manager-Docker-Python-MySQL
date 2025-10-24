#  Task Manager (Flask + Docker + AWS EC2)

A full-stack **Flask Task Manager** web application containerized with **Docker**, deployed on **Amazon EC2**, and integrated with an **auto-creating database** using SQLAlchemy.

---

##  Features
- Flask web app with user authentication & task management
- MySQL / MariaDB backend
- Dockerized for easy deployment
- Auto-database creation on startup
- Nginx reverse proxy configuration
- Compatible with AWS EC2 (Amazon Linux)

---

##  Deployment Steps on AWS EC2 (Amazon Linux)

### 1️ Launch EC2 Instance
1. Go to [AWS EC2 Console]
2. Launch an instance with:
   - **Amazon Linux**
   - **t2.micro** (Free Tier)
   - **Port 22 (SSH)**, **80 (HTTP)**, **443 (HTTPS)** open in Security Group
3. Connect via SSH:
   ```bash
   ssh -i your-key.pem ec2-user@your-ec2-public-ip
   ```

---

### 2️ Update & Install Dependencies
```bash
sudo yum update -y
sudo yum install -y git docker
```

Install Docker Compose:
```bash
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose version
```

Enable Docker service:
```bash
sudo systemctl start docker
sudo systemctl enable docker
```


### 3️ Clone the Project from GitHub
```bash
git clone https://github.com/ChetanMuli/Task-manager-Docker-Python-MySQL.git
cd Task-manager-Docker-Python-MySQL
```


### 4️ Environment Configuration
Copy `.env.example` to `.env` if required:
```bash
cd app
cp .env.example .env
```
### Kindly read .env or docker-compose.yml for database details (Password,User,DB Name)
Adjust DB credentials or secret keys as needed.

---

### 5️ Build and Run Containers
Go back to the main folder where `docker-compose.yml` exists:
```bash
cd ..
docker-compose up -d --build
```

This will:
- Build all Docker images
- Start containers (Flask app, database, Nginx)
- Automatically create database tables

---

### 6️ Verify Deployment
Check running containers:
```bash
docker ps
```

View logs:
```bash
docker logs <container_name>
```

Visit in browser:
```
http://<EC2-Public-IP>
```

You should see your Task Manager web app 

---

### 7️ Common Commands

**Stop containers:**
```bash
docker-compose down
```

**Rebuild (after code changes):**
```bash
docker-compose up -d --build
```

**Check database:**
```bash
docker exec -it <db-container-name or ID> bash
mysql -u <taskuser> -p
```

---

##  Automatic Database Creation

It happens automatically when the container runs.

---


##  License
This project is open-source and free to use for learning and deployment.

---
