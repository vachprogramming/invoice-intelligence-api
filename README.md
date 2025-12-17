# 🧾 Invoice Intelligence (AI-Powered Extraction)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://invoice-intelligence-api.streamlit.app)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)

An AI-powered document processing pipeline that extracts structured data (JSON) from PDF invoices. Built with **Llama-3.2 (via HuggingFace)**, **FastAPI**, and **PostgreSQL**.

---

### 🚀 **Live Demo**
**[Click here to try the App](https://vachprogramming-invoice-intelligence-api-appfrontendui-qohw3h.streamlit.app/)**

> ⚠️ **Note on Free Hosting:**
> The backend is hosted on Render's Free Tier, which "spins down" after inactivity.
> **The first request may take ~60 seconds to wake up the server.**
> Please be patient—subsequent requests will be instant!

---

### 🏗️ Architecture
The system follows a modern decoupled architecture:

1.  **Frontend (Streamlit):** User interface for uploading PDFs.
2.  **Backend (FastAPI):** Handles business logic and validation.
3.  **AI Engine (Llama-3.2-1B):** A lightweight LLM extracts specific fields (Date, Total, Vendor, IBAN).
4.  **Database (PostgreSQL @ Neon):** Asynchronously stores structured invoice data using `SQLAlchemy` + `asyncpg`.

**Tech Stack:**
* **AI/LLM:** HuggingFace Inference API (Llama-3.2-11B-Vision-Instruct)
* **Backend:** FastAPI, Uvicorn, Pydantic
* **Database:** Neon (Serverless PostgreSQL)
* **Infrastructure:** Render (Dockerized Web Service), Streamlit Cloud

---

### 📂 Project Structure
