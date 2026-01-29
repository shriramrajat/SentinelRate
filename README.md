# 🛡️ SentinelRate
**The Infrastructure-Grade Rate Limiter for FastAPI**

> "Rate limiting without identity is blind. Identity without rate limiting is dangerous. Together, they are control."

SentinelRate is a high-performance **Layer 7 Rate Limiting Middleware** designed to protect FastAPI applications from abuse, bursts, and denial-of-service scenarios. Unlike simple decorators, SentinelRate sits at the edge of your application, acting as a decision engine that filters traffic *before* it reaches your business logic.

---

## 🧠 The Philosophy
SentinelRate is built on three core beliefs:
1.  **Identity First**: A rate limiter must know *who* is knocking. Limits for anonymous IPs should be strict; limits for authenticated users should be flexible.
2.  **Stateful, Not Static**: Uses a **Token Bucket** algorithm to allow valid bursts while punishing sustained abuse (simulating real time).
3.  **Zero-Latency Design**: Every microsecond counts. The decision engine is optimized to decide `ALLOW` or `BLOCK` in near-constant time.

---

## ⚡ Key Features
*   **Dual-Resolution Identity**: Automatically detects if a request is from a User (via JWT) or an Anonymous Client (via IP) and applies different policies.
*   **Token Bucket Engine**: Mathematically smooth traffic shaping that handles "bursty" API usage gracefully.
*   **Fail-Closed Architecture**: If the limiter is unsure, it defaults to safety (configurable).
*   **Real-time Metrics**: Built-in `/metrics` endpoint to visualize allowed vs. blocked traffic instantly.
*   **Production Ready Stack**: Built with Python 3.11+, Pydantic v2, and FastAPI.

---

## 🏗️ Architecture
SentinelRate operates as a middleware pipeline:

```mermaid
graph LR
    Client -->|Request| Middleware
    Middleware -->|Extract| Identifier[Resolver (JWT/IP)]
    Identifier -->|Key| Bucket[Token Bucket State]
    Bucket -->|Check| Decision{Allows?}
    Decision --YES--> App[FastAPI Routes]
    Decision --NO--> 429[HTTP 429 Too Many Requests]
```

---

## 🛠️ Quick Start

### 1. Installation
```bash
git clone https://github.com/shriramrajat/SentinelRate.git
cd SentinelRate
pip install -r requirements.txt
```

### 2. Run with Docker
```bash
docker build -t sentinel-rate .
docker run -p 8000:8000 sentinel-rate
```

---

## ⚠️ Status
**Current Version**: `v0.1.0-alpha`
This project is currently under active development. It is designed as a reference implementation for advanced system design patterns.