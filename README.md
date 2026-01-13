# 🏙️ Urban Pulse: Real-Time IoT Sensor Network

![Status](https://img.shields.io/badge/Status-Complete-success)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)
![Python](https://img.shields.io/badge/Python-3.10%2B-yellow)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

**Urban Pulse** is an end-to-end data engineering project that simulates, processes, and visualizes real-time environmental data (AQI & Temperature) from major cities worldwide. 

It demonstrates a modern **Microservices Architecture** using MQTT for high-speed ingestion, Mage AI for orchestration, and a containerized Frontend/Backend for visualization.

---

## 🏗️ Architecture

The system follows a standard ETL (Extract, Transform, Load) pipeline pattern:

```mermaid
graph LR
    A[Python Simulator] -- MQTT --> B[RabbitMQ Broker]
    B -- Stream --> C[Mage AI]
    C -- ETL --> D[PostgreSQL DB]
    D -- SQL --> E[FastAPI Backend]
    E -- JSON --> F[Streamlit Dashboard]