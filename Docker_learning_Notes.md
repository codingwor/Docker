# 🐳 Docker — Complete Beginner to Practical Guide

> A complete, beginner-friendly reference for learning Docker from scratch with real examples, commands, and explanations.

---

## 📚 Table of Contents

1. [What is Docker?](#-what-is-docker)
2. [Core Concepts](#-core-concepts)
3. [Basic Commands](#-basic-commands)
4. [Images](#-images)
5. [Containers](#-containers)
6. [Port Mapping](#-port-mapping)
7. [Volume Mapping](#-volume-mapping)
8. [Dockerfile](#-dockerfile)
9. [CMD vs ENTRYPOINT](#-cmd-vs-entrypoint)
10. [Environment Variables](#-environment-variables)
11. [Docker Compose](#-docker-compose)
12. [Docker Registry](#-docker-registry)
13. [Docker Engine](#-docker-engine)
14. [Docker Storage](#-docker-storage)
15. [Docker Networking](#-docker-networking)
16. [Container Orchestration & Docker Swarm](#-container-orchestration--docker-swarm)
17. [Quick Reference Cheatsheet](#-quick-reference-cheatsheet)

---

## 🤔 What is Docker?

Docker is a platform that packages your application and everything it needs (code, runtime, libraries, config) into a **container** — a single unit that runs the same on any machine.

```
Without Docker:  "It works on my machine!" 😭
With Docker:     "It works everywhere!" 🎉
```

### The Big Picture

```
Dockerfile  ──► docker build ──► Image ──► docker run ──► Container
(recipe)                        (template)               (running app)
```

| Term           | Analogy                 | Meaning                         |
| -------------- | ----------------------- | ------------------------------- |
| **Dockerfile** | Recipe                  | Instructions to build an image  |
| **Image**      | Cake mold / Blueprint   | Read-only template              |
| **Container**  | Running cake / Instance | Live, running copy of the image |
| **Registry**   | App store               | Place to store & share images   |

---

## 🧠 Core Concepts

### Image vs Container

```
Image  = class in programming    (read-only, reusable)
Container = object / instance    (running, isolated, writable)
```

One image → many containers running from it simultaneously.

### Layered Architecture

```
┌─────────────────────────────┐
│   Container Layer (R/W)      │  ← thin writable layer, deleted with container
├─────────────────────────────┤
│   Image Layer N  (R/O)       │
│   Image Layer 2  (R/O)       │  ← cached, shared across containers
│   Image Layer 1  (R/O)       │
└─────────────────────────────┘
```

Docker caches each layer. If only your `app.py` changes, Docker reuses all previous cached layers — making rebuilds **much faster**.

---

## ⌨️ Basic Commands

### Container Lifecycle

```bash
docker run image_name           # pull + create + start a container
docker pull image_name          # only download image, don't run it
docker run redis:4.0            # ':4.0' is a TAG — specifies a version
docker ps                       # list RUNNING containers
docker ps -a                    # list ALL containers (running + stopped)
docker stop name/id             # gracefully stop a running container
docker kill name/id             # force-stop immediately
docker rm name/id               # delete a stopped container
docker rename OLD NEW           # rename a container
docker restart name/id          # restart a container
```

### Info & Debugging

```bash
docker logs container_name               # view container output logs
docker logs -f container_name            # follow logs in real-time
docker logs --since=10m container_name   # logs from past 10 minutes
docker inspect container_name            # full JSON details (IP, mounts, env...)
docker stats                             # live CPU/RAM usage of all containers
docker exec -it container_id bash        # open a shell inside running container
docker cp container:/path /host/path     # copy files between container and host
docker info                              # Docker system-level info
```

### Cleanup

```bash
docker image prune        # remove unused/dangling images
docker container prune    # remove ALL stopped containers
docker volume prune       # remove unused volumes
docker system prune       # clean everything unused (images, containers, networks)
```

> 💡 **Flags Explained:**
>
> - `-a` → All (running + stopped)
> - `-q` → Quiet — only show IDs (great for scripting)
> - `-f` → Follow (for logs) / Force (for removal)

---

## 🖼️ Images

Images are **read-only templates** containing everything needed to run an application — OS, dependencies, code, configs.

```bash
docker images               # list all local images
docker rmi image_name       # remove an image
docker history image_name   # show layer-by-layer build history
docker image prune          # remove all unused images
```

> ⚠️ Before removing an image, you must first remove all containers that use it.

```bash
# Safe removal workflow
docker ps -a                 # find containers using the image
docker rm container_name     # remove container(s) first
docker rmi image_name        # now safely remove the image
```

---

## 📦 Containers

A container is an **isolated environment** where your application runs, without affecting anything outside it.

### Key Run Flags

```bash
docker run nginx                            # run in foreground (blocks terminal)
docker run -d nginx                         # detached: run in background
docker run -it ubuntu bash                  # interactive shell inside container
docker run --name myapp nginx               # give container a custom name
docker run --rm ubuntu echo "hello"         # auto-delete container after it exits
docker run ubuntu sleep 10                  # keep container alive for 10 seconds
```

### Flags Explained

| Flag     | Long Form       | Meaning                                          |
| -------- | --------------- | ------------------------------------------------ |
| `-d`     | `--detach`      | Run in background                                |
| `-i`     | `--interactive` | Keep STDIN open (for typing)                     |
| `-t`     | `--tty`         | Allocate a terminal interface                    |
| `-it`    | both            | Interactive terminal (most common for debugging) |
| `--rm`   | —               | Auto-remove container on exit                    |
| `--name` | —               | Assign a name to the container                   |

### Attach vs Exec

```bash
docker attach container_id          # reconnect to the main process's stdin/stdout
docker exec -it container_id bash   # start a NEW process inside running container ✅ preferred
```

> 💡 Use `docker exec` for debugging — it doesn't interrupt your running app.

---

## 🔌 Port Mapping

By default, a container's network is **isolated** — nothing outside can reach it. Port mapping creates a doorway.

```bash
docker run -p 8080:5000 webapp
#            ^^^^  ^^^^
#           HOST  CONTAINER
```

```
User browser → localhost:8080 → Docker → container:5000 → Flask app
```

**Mental Model:** Left = your laptop's door. Right = the container's internal door.

```bash
docker run -p 80:80 nginx          # map host port 80 to container port 80
docker run -p 3000:3000 myapp      # map port 3000 to port 3000
docker run -p 8080:80 webapp       # host 8080 → container 80 (different ports)
```

---

## 💾 Volume Mapping

Containers are **ephemeral** — delete the container, lose all data inside it. Volumes solve this.

### Why Volumes Matter

```
Without Volume:  Delete container → lose all database data 😱
With Volume:     Delete container → data still on your host machine ✅
```

### Types of Volume Mounting

#### 1. Named Volume (Recommended for production)

```bash
docker volume create data_volume
docker run -v data_volume:/var/lib/mysql mysql
# Docker manages the storage at /var/lib/docker/volumes/data_volume/
```

#### 2. Bind Mount (Recommended for development)

```bash
# Old syntax (-v)
docker run -v /opt/datadir:/var/lib/mysql mysql

# New syntax (--mount) - more explicit, preferred
docker run --mount type=bind,source=/opt/datadir,target=/var/lib/mysql mysql
```

#### 3. Summary

| Type         | Who Controls Path | Best For                     |
| ------------ | ----------------- | ---------------------------- |
| Named volume | Docker            | Databases, production data   |
| Bind mount   | You               | Development (live code sync) |

```bash
docker volume create my_vol       # create a named volume
docker volume ls                  # list all volumes
docker volume inspect my_vol      # see volume details
docker volume rm my_vol           # remove a volume
```

> 💡 With bind mounts: files created on host → visible in container, and vice versa — instantly.

---

## 📝 Dockerfile

A Dockerfile is a **recipe** — a text file with step-by-step instructions Docker follows to build an image.

### Complete Annotated Dockerfile

```dockerfile
# Step 1: Start from a base image (always required first line)
# 'slim' = lightweight Debian variant — smaller image size
FROM python:3.11-slim

# Step 2: Set the working directory inside the container
# All subsequent commands run from here
WORKDIR /app

# Step 3: Copy requirements BEFORE code (Docker layer caching trick)
# If only app.py changes, Docker reuses the cached pip install layer ✅
COPY requirements.txt .

# Step 4: Install dependencies during BUILD (not runtime)
# --no-cache-dir keeps the image smaller
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy remaining app code into container
COPY . .

# Step 6: Set environment variables (optional)
ENV APP_COLOR=blue

# Step 7: Document which port the app listens on (informational only)
EXPOSE 5000

# Step 8: The command to run when the container STARTS
CMD ["python", "app.py"]
```

### Build Commands

```bash
docker build .                            # build using current directory
docker build -t myapp .                   # build and name the image 'myapp'
docker build -t myapp:v2 .               # build with version tag
docker build -f MyDockerfile -t myapp .   # use a custom-named Dockerfile
```

> 💡 `.` (dot) = the **build context** — the folder of files Docker can access during build.

### Dockerfile Instructions Reference

| Instruction  | Purpose                                  | Example                       |
| ------------ | ---------------------------------------- | ----------------------------- |
| `FROM`       | Base image (required first)              | `FROM ubuntu`                 |
| `RUN`        | Execute command at build time            | `RUN apt-get install -y curl` |
| `COPY`       | Copy files from host to image            | `COPY . /app`                 |
| `ADD`        | Like COPY but also handles URLs/tarballs | `ADD app.tar.gz /app`         |
| `WORKDIR`    | Set working directory                    | `WORKDIR /app`                |
| `ENV`        | Set environment variable                 | `ENV PORT=5000`               |
| `EXPOSE`     | Document the port (informational)        | `EXPOSE 5000`                 |
| `ENTRYPOINT` | Fixed command, always runs               | `ENTRYPOINT ["python"]`       |
| `CMD`        | Default args (overridable)               | `CMD ["app.py"]`              |
| `VOLUME`     | Create a mount point                     | `VOLUME /data`                |

### .dockerignore

Like `.gitignore` — tells Docker NOT to copy these files into the image:

```
__pycache__
*.pyc
.git
.env
venv
node_modules
```

---

## ⚙️ CMD vs ENTRYPOINT

This is one of the trickiest Docker concepts — let's nail it with a clear table.

```dockerfile
FROM ubuntu
ENTRYPOINT ["sleep"]
CMD ["5"]
```

| Command                                              | Result        | Explanation                  |
| ---------------------------------------------------- | ------------- | ---------------------------- |
| `docker run ubuntu-sleeper`                          | `sleep 5`     | CMD provides default arg     |
| `docker run ubuntu-sleeper 10`                       | `sleep 10`    | `10` REPLACES CMD's `5`      |
| `docker run --entrypoint sleep2.0 ubuntu-sleeper 10` | `sleep2.0 10` | ENTRYPOINT itself overridden |

### Rule of Thumb

```
ENTRYPOINT = the fixed program (hard to change)
CMD        = default arguments (easy to override)
```

```dockerfile
# Only CMD — entire CMD replaced when you pass args
CMD ["sleep", "5"]

# ENTRYPOINT + CMD — CMD acts as default args to ENTRYPOINT
ENTRYPOINT ["sleep"]
CMD ["5"]
```

---

## 🌍 Environment Variables

Instead of hardcoding values, use environment variables to make containers configurable.

### In your app code

```python
# app.py
import os
color = os.environ.get('APP_COLOR', 'red')   # 'red' = fallback default
```

### Pass variables at runtime

```bash
docker run -e APP_COLOR=blue simple-webapp-color
docker run -e APP_COLOR=green -e DEBUG=true myapp   # multiple vars
```

### Check existing env vars in a container

```bash
docker inspect container_name   # look for the "Env" section in JSON output
```

### Use an env file

```bash
# .env file
APP_COLOR=blue
PORT=5000

docker run --env-file .env myapp
```

---

## 🎼 Docker Compose

Docker Compose lets you define and run **multiple containers** using a single `docker-compose.yml` file.

```
Without Compose:  docker run redis + docker run web + docker network create ... 😵
With Compose:     docker-compose up  ✅
```

### Complete docker-compose.yml

```yaml
version: "3.8"

services:
  # ── Web App (Flask) ─────────────────────────────
  web:
    build: . # build image from Dockerfile in current dir
    ports:
      - "5000:5000" # host:container
    volumes:
      - .:/app # bind mount for live code sync
    environment:
      - APP_COLOR=blue
    depends_on:
      - redis # start redis BEFORE web (not "wait until ready")

  # ── Redis Database ───────────────────────────────
  redis:
    image: redis:alpine # pull pre-built image, no Dockerfile needed

  # ── PostgreSQL ───────────────────────────────────
  db:
    image: postgres
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: mydb
    volumes:
      - db_data:/var/lib/postgresql/data # persist database data

# Named volumes must be declared here
volumes:
  db_data:
```

### Compose Commands

```bash
docker-compose up                   # build + create + start all services
docker-compose up -d                # detached (background) mode
docker-compose up --build           # force rebuild images before starting
docker-compose down                 # stop + remove containers and networks
docker-compose down -v              # also delete named volumes (full reset)
docker-compose ps                   # list containers managed by this file
docker-compose logs -f              # follow logs from all services
docker-compose logs web             # logs from specific service
docker-compose exec web bash        # shell into a running service
docker-compose restart web          # restart one service
docker-compose stop                 # stop without removing
```

### How Containers Find Each Other

All services in one Compose file share a **private network** automatically. Each service is reachable by its **service name as a hostname**:

```python
# In your app.py, connect to redis like this:
cache = redis.Redis(host='redis', port=6379)
#                          ^^^^^
#                          Service name from docker-compose.yml
```

Docker's built-in DNS (Embedded DNS) resolves `redis` → the container's IP automatically.

---

## 📦 Docker Registry

A registry is a **storage and distribution system for Docker images**.

```
Local machine → Push → Registry → Pull → Any other machine
```

### Docker Hub (Public Registry)

```bash
docker login                                  # login to Docker Hub
docker tag myapp username/myapp:v1            # tag image with your username
docker push username/myapp:v1                 # push to Docker Hub
docker pull username/myapp:v1                 # pull from anywhere in the world
```

### Image Name Anatomy

```
docker.io  /  library  /  redis  :  alpine
   ^              ^         ^          ^
Registry    Namespace    Image     Version tag
```

- `docker.io` = Docker Hub (default registry, can be omitted)
- `library` = official verified images (can be omitted for official images)

### Private Registry

```bash
# Use someone else's private registry
docker login private-registry.io
docker run private-registry.io/apps/internal-app

# Host YOUR OWN private registry
docker run -d -p 5000:5000 --name registry registry:2

# Tag & push to your local registry
docker image tag myapp localhost:5000/myapp
docker push localhost:5000/myapp

# Pull from your local registry
docker pull localhost:5000/myapp
```

|            | Public Registry    | Private Registry         |
| ---------- | ------------------ | ------------------------ |
| Location   | Docker Hub (cloud) | Your own server          |
| Access     | Anyone             | Only inside your network |
| Tag format | `username/app`     | `ip:5000/app`            |

---

## ⚙️ Docker Engine

Docker is a **client-server** architecture:

```
┌────────────┐    REST API    ┌────────────────────┐
│  Docker CLI │ ──────────── ► │  Docker Daemon     │
│  (Client)   │               │  (dockerd, Server) │
│  Your laptop│               │  Does the real work│
└────────────┘               └────────────────────┘
```

### Remote Docker Engine

```bash
# Run containers on a REMOTE machine from your laptop
docker -H=10.123.2.1:2375 run nginx
#         ^^^^^^^^^^^^^^
#         Remote server IP and port

# Flow:
# CLI on laptop → REST API → Daemon on remote server → Container starts there
```

### Namespaces & Cgroups (How Isolation Works)

**Namespaces** = what a container _can see_ (isolation):

```
Host PID 1
├── Host PID 2
├── Host PID 3  ← Container thinks this is PID 1 (its own "PID 1")
│   └── Host PID 4  ← Container sees as PID 2
└── Host PID 5
```

Each container gets its own: PID space, network stack, filesystem root, hostname.

**Cgroups** = what a container _can use_ (resource limits):

```bash
docker run --cpus=0.5 ubuntu       # max 50% of one CPU core
docker run --memory=100m ubuntu    # max 100MB RAM
```

> 💡 **Analogy:** Namespaces = each school classroom can't see other classrooms (isolation). Cgroups = each classroom has a max student limit (resource limits).

---

## 🗄️ Docker Storage

### Copy-on-Write Mechanism

```
Image layer (Read-Only)  →  contains app.py
Container layer (R/W)    →  if you edit app.py, Docker copies it here first
                             original image layer is NEVER modified
```

If you want permanent changes to an image — **rebuild it**, not edit a running container.

### Storage Drivers

Storage drivers manage how image layers are merged and presented as one filesystem.

| Driver          | Status                                     |
| --------------- | ------------------------------------------ |
| `overlay2`      | ✅ Default and recommended on modern Linux |
| `aufs`          | Older, still used on some systems          |
| `btrfs` / `zfs` | Advanced, specific use cases               |

You rarely need to configure this — `overlay2` just works.

---

## 🌐 Docker Networking

### The 4 Network Types

#### 1. Bridge (Default)

```bash
docker run nginx                          # automatically uses bridge
docker run -p 8080:80 nginx               # expose to outside via port mapping
```

- Default network every container joins
- Containers get internal IPs like `172.17.0.x`
- Must use port mapping (`-p`) to expose to host

#### 2. Host

```bash
docker run --network=host nginx
```

- Container shares the host's network stack directly
- Port 80 in container = port 80 on host (no mapping needed)
- Downside: no network isolation

#### 3. None

```bash
docker run --network=none alpine
```

- Completely isolated — zero network access
- Good for pure compute jobs

#### 4. User-Defined Bridge (Best for multi-container apps)

```bash
docker network create --driver bridge --subnet 182.18.0.0/16 my-network
docker run --network=my-network --name web nginx
docker run --network=my-network --name api myapi
# 'web' can now reach 'api' by name ✅
```

### Embedded DNS

Docker has a built-in DNS server. On user-defined networks (including Compose networks), containers can reach each other by **name** — not by IP (IPs change, names don't).

```bash
# From inside the 'web' container:
ping api        # works on user-defined network ✅
ping 172.18.0.3 # also works but fragile (IP can change)
```

### Network Commands

```bash
docker network ls                    # list all networks
docker network create my-net         # create a custom network
docker network inspect bridge        # see containers and their IPs
docker network connect my-net myapp  # connect running container to a network
docker network rm my-net             # remove a network
```

---

## 🚀 Container Orchestration & Docker Swarm

When you have **many containers across many machines**, you need orchestration to manage them.

### What Orchestration Solves

```
Without Orchestration:
  - Containers crash → stays dead
  - Heavy traffic → you manually start more containers
  - Machine fails → you manually move containers

With Orchestration (Swarm / Kubernetes):
  - Container crashes → auto-restart ✅
  - Heavy traffic → auto-scale up ✅
  - Machine fails → auto-move containers to healthy machine ✅
```

### Docker Swarm

```bash
# On the manager machine:
docker swarm init

# On worker machines (use the token shown above):
docker swarm join --token <TOKEN> <MANAGER_IP>:2377

# Create a service (managed group of containers)
docker service create --name web -p 8080:80 nginx

# Scale to 3 replicas (3 containers across your machines)
docker service create --replicas=3 my-web-app

# Scale up/down on the fly
docker service scale web=5

# List all machines in the swarm
docker node ls

# List running services
docker service ls
```

### Swarm vs Kubernetes

|                | Docker Swarm           | Kubernetes            |
| -------------- | ---------------------- | --------------------- |
| Complexity     | Simple ✅              | Complex               |
| Learning curve | Low                    | High                  |
| Production use | Small–medium           | Industry standard     |
| Setup          | Built into Docker      | Separate install      |
| Best for       | Learning orchestration | Real-world production |

---

## 📋 Quick Reference Cheatsheet

### Most Used Commands Daily

```bash
# === IMAGES ===
docker images                     # list local images
docker pull nginx                 # download image
docker build -t myapp .           # build image from Dockerfile
docker rmi myapp                  # delete image

# === CONTAINERS ===
docker run -d -p 8080:80 --name web nginx   # run in background with port + name
docker ps                          # running containers
docker ps -a                       # all containers
docker stop web                    # stop container
docker rm web                      # delete container
docker logs -f web                 # follow logs
docker exec -it web bash           # shell into container

# === VOLUMES ===
docker volume create mydata
docker run -v mydata:/data myapp
docker run -v $(pwd):/app myapp    # bind mount current dir

# === NETWORKS ===
docker network create mynet
docker run --network mynet --name api myapp

# === COMPOSE ===
docker-compose up -d               # start all services
docker-compose down                # stop all services
docker-compose logs -f             # follow logs
docker-compose exec web bash       # shell into service

# === CLEANUP ===
docker system prune                # remove all unused stuff
docker rm $(docker ps -aq)         # delete all containers
docker rmi $(docker images -q)     # delete all images
```

### Common Dockerfile Pattern

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

### Project Structure

```
my-project/
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .dockerignore
```

---

### How to run the project

```
# Build images and start both containers in the foreground
docker-compose up

# Or run in background (detached mode)
docker-compose up -d
```

Then open http://localhost:5000 in your browser — refresh a few times and watch the counter increase (proving the Flask container and Redis container are communicating).

```
# Stop and remove containers, networks created by 'up'
docker-compose down

# Stop and ALSO delete the Redis data volume (full reset)
docker-compose down -v
```

---

## 📖 Learning Path for Beginners

1. ✅ **Run your first container:** `docker run hello-world`
2. ✅ **Explore inside a container:** `docker run -it ubuntu bash`
3. ✅ **Build an image:** Write a Dockerfile, run `docker build`
4. ✅ **Port mapping:** Expose a web app and visit it in a browser
5. ✅ **Volumes:** Persist database data across container restarts
6. ✅ **Docker Compose:** Run a web app + database together
7. ✅ **Push to Docker Hub:** Share your image with the world
8. ✅ **Custom networks:** Two containers talking by name
9. ✅ **Docker Swarm:** Scale a service to multiple replicas
