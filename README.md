
# 🚀 MicroStack

A lightweight, production-grade microservices system using **FastAPI**, **PostgreSQL**, **Redis**, and **Docker Compose**.

---

## ⚙️ Core Functionality

### 🧑‍💼 User Service (`/users`)

* Built with **FastAPI**
* Integrated with **PostgreSQL** for persistent user data
* Implements complete **CRUD operations** for user management
* Includes a **robust retry mechanism** for reliable database connections
* Environment configuration is securely handled via `.env` using `python-dotenv`

---

### 📦 Order Service (`/orders`)

* Built with **FastAPI**
* Integrated with **PostgreSQL** for order persistence
* Implements complete **CRUD operations** for order processing
* Includes a **retry mechanism** to gracefully handle DB startup delays or failures
* Secure environment variable loading with `.env` using `python-dotenv`

---

## 🐳 Dockerized Microservices

* Each microservice is containerized using **Docker**
* **Docker Compose** is used for service orchestration
* **PostgreSQL** and **Redis** are provisioned as independent containers
* Services are designed to start independently with support for retries and health checks

---

## 🔐 Environment Config

* All sensitive credentials (DB, Redis) are managed via `.env` files
* `.env.example` templates are included for easy setup
* Secure, production-aligned practices applied for config management

---
