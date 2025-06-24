# 🚀 MicroStack

A lightweight, production-grade microservices system using **FastAPI**, **PostgreSQL**, **Redis**, and **Docker Compose**.

---

## ⚙️ Core Functionality

### 🧑‍💼 User Service (`/users`)
- Built with **FastAPI**
- Connects to **PostgreSQL**
- Returns a static response from a DB query to verify connectivity
- Loads DB credentials securely from `.env` via `python-dotenv`

### 📦 Order Service (`/orders`)
- Built with **FastAPI**
- Connects to **Redis**
- Fetches and returns `recent_order` from Redis cache
- Uses `.env` and `python-dotenv` for secure Redis config

---

## 🐳 Dockerized Microservices

- Each service has its own **Dockerfile**
- Services are orchestrated using **Docker Compose**
- PostgreSQL and Redis run as separate containers

---

## 🔐 Environment Config

- All sensitive values are stored in `.env` files (excluded via `.gitignore`)
- Sample config provided via `.env.example` files in each service

---

## ▶️ Endpoints

| Service        | Endpoint             | Description                   |
|----------------|----------------------|-------------------------------|
| User Service   | `/users`             | Returns a message from DB     |
| Order Service  | `/orders`            | Returns cached Redis value    |

---
