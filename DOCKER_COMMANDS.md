# 🐳 Docker Commands — file-sharing-app

> **Docker Hub Username:** `ashleyalmeida410`
> **Image Name:** `file-sharing-app`
> **Container Name:** `file-sharing-container`
> **Port:** `5000`

---

## 🔨 Build

```bash
# Build the Docker image
docker build -t file-sharing-app .

# Build with a specific tag/version
docker build -t file-sharing-app:v1.0 .

# Build without using cache (fresh build)
docker build --no-cache -t file-sharing-app .
```

---

## 🏷️ Tag

```bash
# Tag for Docker Hub (latest)
docker tag file-sharing-app ashleyalmeida410/file-sharing-app:latest

# Tag with a version number
docker tag file-sharing-app ashleyalmeida410/file-sharing-app:v1.0
```

---

## 🔐 Login

```bash
# Login to Docker Hub
docker login

# Login with username directly
docker login -u ashleyalmeida410

# Logout
docker logout
```

---

## 📤 Push

```bash
# Push latest to Docker Hub
docker push ashleyalmeida410/file-sharing-app:latest

# Push a specific version
docker push ashleyalmeida410/file-sharing-app:v1.0
```

---

## 📥 Pull

```bash
# Pull latest image from Docker Hub
docker pull ashleyalmeida410/file-sharing-app:latest

# Pull a specific version
docker pull ashleyalmeida410/file-sharing-app:v1.0
```

---

## ▶️ Run

```bash
# Run in detached mode (background)
docker run -d --name file-sharing-container -p 5000:5000 file-sharing-app

# Run with volume (uploads persist after container stops)
docker run -d --name file-sharing-container -p 5000:5000 -v ${PWD}/uploads:/app/uploads file-sharing-app

# Run from Docker Hub image
docker run -d --name file-sharing-container -p 5000:5000 ashleyalmeida410/file-sharing-app:latest

# Run interactively (see logs in terminal)
docker run -it --name file-sharing-container -p 5000:5000 file-sharing-app
```

> 🌐 Open in browser: **http://localhost:5000**

---

## ⏯️ Start / Stop / Restart

```bash
# Start a stopped container
docker start file-sharing-container

# Stop a running container
docker stop file-sharing-container

# Restart the container
docker restart file-sharing-container
```

---

## 📋 Logs & Status

```bash
# View container logs
docker logs file-sharing-container

# Follow logs in real time
docker logs -f file-sharing-container

# List all running containers
docker ps

# List all containers (including stopped)
docker ps -a

# List all local images
docker images
```

---

## 🗑️ Cleanup

```bash
# Remove the container
docker rm file-sharing-container

# Force remove a running container
docker rm -f file-sharing-container

# Remove the image
docker rmi file-sharing-app

# Remove Docker Hub tagged image
docker rmi ashleyalmeida410/file-sharing-app:latest

# Remove all stopped containers
docker container prune

# Remove all unused images
docker image prune

# Remove everything (containers, images, networks, cache)
docker system prune -a
```

---

## 🔁 Full Workflow (Build → Push → Pull → Run)

```bash
# Step 1: Build
docker build -t file-sharing-app .

# Step 2: Tag
docker tag file-sharing-app ashleyalmeida410/file-sharing-app:latest

# Step 3: Login
docker login

# Step 4: Push
docker push ashleyalmeida410/file-sharing-app:latest

# --- On any other machine ---

# Step 5: Pull
docker pull ashleyalmeida410/file-sharing-app:latest

# Step 6: Run
docker run -d --name file-sharing-container -p 5000:5000 ashleyalmeida410/file-sharing-app:latest
```

---

## 🔗 Docker Hub

- **Repository:** https://hub.docker.com/r/ashleyalmeida410/file-sharing-app
