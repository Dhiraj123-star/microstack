# 🚀 MicroStack

A lightweight, production-grade microservices system using **FastAPI**, **PostgreSQL**, **Redis**, **Nginx**, and **Docker Compose** — fully containerized, cache-optimized, and secured with **HTTPS**. 🌐🔐

---

## ⚙️ Core Functionality

### 🧑‍💼 User Service (`/users`)

- Built with **FastAPI**
- Integrated with **PostgreSQL** for persistent user data
- Complete **CRUD operations** for user management
- Uses **Redis caching** for optimized GET requests
- Automatically **invalidates cache** on create, update, and delete operations
- Implements **robust retry mechanism** for reliable DB connection
- Loads configuration via `.env` using `python-dotenv`
- Exposed behind **Nginx reverse proxy** over **HTTPS**
- Swagger: `https://localhost/users/docs`

---

### 📦 Order Service (`/orders`)

- Built with **FastAPI**
- Integrated with **PostgreSQL** for order persistence
- Full **CRUD operations** for orders
- Validates `user_id` via internal HTTP call to **User Service**
- Uses **Redis cache** for GET requests
- Cache is **invalidated** on any DB write (create/update/delete)
- Retry mechanism ensures DB readiness at startup
- Config managed via `.env` and `python-dotenv`
- Exposed through **Nginx reverse proxy** over **HTTPS**
- Swagger: `https://localhost/orders/docs`

---

## 🐳 Dockerized & Orchestrated

- All services containerized using **Docker**
- **Docker Compose** for orchestration
- Each service has a dedicated **PostgreSQL** instance
- Shared **Redis** container for caching
- **Nginx** routes traffic and serves SSL
- Retry logic ensures services wait for DB readiness
- HTTPS enabled via **self-signed SSL certificates**

---

## 🔁 CI/CD with GitHub Actions

- **Automatic Docker image build & push** on every commit to `main` branch
- Leverages GitHub Actions for seamless CI/CD
- Publishes Docker images to **[dhiraj918106/microstack](https://hub.docker.com/r/dhiraj918106/microstack)**
- Keeps the build process consistent and production-ready

---

Made with ❤️ using FastAPI, PostgreSQL, Redis, and Docker — now HTTPS & CI/CD ready! 🚀
