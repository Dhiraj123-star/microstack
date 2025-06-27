
# 🚀 MicroStack

A lightweight, production-grade microservices system using **FastAPI**, **PostgreSQL**, **Redis**, **Nginx**, and **Docker Compose** — fully containerized and secured with **HTTPS**. 🌐🔐

---

## ⚙️ Core Functionality

### 🧑‍💼 User Service (`/users`)

- Built with **FastAPI**
- Integrated with **PostgreSQL** for persistent user data
- Complete **CRUD operations** for user management
- Includes a **robust retry mechanism** for database connection reliability
- Configured via `.env` with `python-dotenv`
- Mounted under `/users` path behind **Nginx reverse proxy**
- Fully accessible via **HTTPS**
- Swagger docs: `https://localhost/users/docs`

---

### 📦 Order Service (`/orders`)

- Built with **FastAPI**
- Integrated with **PostgreSQL** for order persistence
- Full **CRUD functionality** for orders
- Implements **retry logic** for handling DB readiness
- Uses **HTTP call to User Service** to validate `user_id` before order creation
- Prevents creation of orders for non-existent users
- Managed securely via `.env` and `python-dotenv`
- Mounted under `/orders` path via **Nginx reverse proxy**
- Exposed over **HTTPS**
- Swagger docs: `https://localhost/orders/docs`

---

## 🐳 Dockerized Services & Orchestration

- Microservices and dependencies are containerized with **Docker**
- **Docker Compose** used for orchestration
- Independent PostgreSQL DB containers for each service
- Redis included for caching/future use
- Services implement **startup retries** for database readiness
- Centralized routing and SSL handled by **Nginx**

---

## 🌐 HTTPS via Nginx

- **Nginx** serves as a reverse proxy for all services
- Routes:
  - `/users` → `user_service`
  - `/orders` → `order_service`
- Supports **HTTPS with self-signed SSL certificates**
- ✅ Valid SSL configuration enables full Swagger UI and secure API access
- 🔐 Certificates (`.crt`, `.key`) are **ignored from version control** using `.gitignore`

---


Made with ❤️ using FastAPI, PostgreSQL, and Docker — now HTTPS-ready! 🚀

