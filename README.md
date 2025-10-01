# JobFit-Analyzer

**JobFit-Analyzer** is an AI-powered Resume Analyzer that evaluates a candidate’s resume against a given job description.  
It provides insights into **strengths**, **weaknesses**, and **suggestions for improvement**, helping candidates align their profiles with specific job roles.

---

## 🚀 Features

- 📄 **Resume Upload** – Upload resumes in PDF format
- 🧾 **Job Description Input** – Provide a JD along with the resume
- 🤖 **AI-Powered Analysis** – Uses LLM (e.g., OpenAI GPT) to compare resume and JD
- 💡 **Insights & Feedback** – Returns key strengths, weaknesses, and recommendations
- 📬 **Queue Processing** – Asynchronous background job handling with RQ and Valkey/Redis
- 🗃 **MongoDB Integration** – Stores resumes, job descriptions, and processing results

---

## 🏗️ Architecture Overview

- **FastAPI** – Web framework for API endpoints
- **MongoDB** – Stores file metadata and job descriptions
- **RQ (Redis Queue)** – Handles background jobs (file parsing, AI analysis)
- **Valkey/Redis** – Message broker for RQ
- **pdf2image** + **poppler-utils** – Convert PDF resumes to text
- **OpenAI API** – Used to analyze and generate insights

---

## ⚙️ Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/yourusername/resumealign.git
cd resumealign
```

### 2️⃣ Create and activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
```
### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```
### Start RQ Worker
```bash
rq worker -u redis://localhost:6379 default
```
### 🌐 Access the API
Open your browser at:
👉 http://localhost:8000/docs

You can explore all endpoints interactively using Swagger UI.


