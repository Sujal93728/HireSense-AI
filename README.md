# 🚀 HireSense AI

An AI-powered Job Recommendation and Resume Analysis platform that helps job seekers improve their resumes, discover relevant jobs, and receive personalized career guidance using Large Language Models.

---

## ✨ Features

- 📄 Resume ATS Score
- 🤖 AI Resume Reviewer
- 💼 Job Recommendation System
- 🎯 Skill Gap Analysis
- 🧠 Career Assistant Chatbot
- 📝 Resume Builder
- 💰 Salary Prediction
- 🔍 Job Search
- 📊 Dashboard

---

## 🛠 Tech Stack

### Frontend
- React.js
- Vite
- JavaScript
- CSS

### Backend
- FastAPI
- Python
- PostgreSQL

### AI & Machine Learning
- Groq Llama 3.3
- FAISS
- Sentence Transformers
- Scikit-learn

### Database
- PostgreSQL

---

## 📂 Project Structure

```text
HireSense-AI
│
├── backend/
│   ├── app/
│   ├── faiss/
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── components/
│   └── pages/
│
├── dataset/
│   ├── sample_jobs.csv
│   ├── sample_companies.csv
│   └── README.md
│
├── screenshots/
│
└── README.md
```

---

## ⚙ Installation

### Clone

```bash
git clone https://github.com/Sujal93728/HireSense-AI.git
cd HireSense-AI
```

### Backend

```bash
cd backend

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt
```

Create a `.env` file:

```env
DATABASE_URL=YOUR_DATABASE_URL
GROQ_API_KEY=YOUR_GROQ_API_KEY
```

Start the backend:

```bash
uvicorn app.main:app --reload
```

---

### Frontend

```bash
cd frontend

npm install

npm run dev
```

---

## 📊 Dataset

This repository contains only **sample datasets**.

Download the complete LinkedIn Job Posting dataset from Kaggle and place it inside the `dataset` folder.

---

## 🔮 Future Improvements

- Authentication
- Email notifications
- AI Interview Preparation
- Resume PDF Export
- Company Analytics
- Docker Deployment
- Cloud Hosting

---

## 👨‍💻 Author

**Sujal**

GitHub:
https://github.com/Sujal93728

---

## ⭐ If you like this project

Give it a ⭐ on GitHub.