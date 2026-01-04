# 🎯 Bravo Academy & IQ Test Platform

A high-performance, secure, and professional-grade IQ Test Platform designed for the **Bangladesh Bravo Academy**. This project was specifically engineered to help candidates of the **Bangladesh Armed Forces (Army, Navy, Air Force)** prepare for the **ISSB (Inter Services Selection Board)** exams through rigorous, timed IQ evaluations.

---

## 📖 The Mission

This platform was developed as a specialized digital solution for a university senior who is establishing a **Defense Coaching Center**. The primary objective is to bridge the gap between traditional coaching and the high-stakes digital testing environment of actual ISSB trials. 

Candidates are provided with a realistic, high-pressure testing environment that mirrors the actual 100-question, 30-minute IQ trials found in Armed Forces selection boards.

---

## 🚀 Key Features

### 🧠 Advanced Testing Engine
- **Timed ISSB Simulations:** Precise 30-minute timers with backend-enforced auto-submission to ensure strict time limit compliance.
- **Extensive Question Bank:** Supports massive datasets (Set 1 includes 100 distinct questions) with randomized delivery and category-based sorting.
- **Public & Private Access:** Features a "Free Sample" mode for public engagement and a "Member Only" portal for enrolled academy students.

### 🛡️ Enterprise-Grade Security
- **One-Device Restriction:** Sophisticated device fingerprinting ensures that a single user account cannot be used across multiple devices simultaneously, preventing unauthorized account sharing.
- **Secure Authentication:** JWT-based architecture with short-lived access tokens and secure rotation-enabled refresh tokens.
- **Advanced Hashing:** Utilizes **Argon2**, the winner of the Password Hashing Competition, for maximum database security.

### 📊 Performance Analytics
- **Recalculation Engine:** A robust backend system that analyzes raw test data to calculate complex metrics such as **Accuracy Trends, Average Speed, and Total Time Invested.**
- **Student Dashboard:** Real-time data visualization showing progress over time and comparative performance.
- **Admin Portal:** A full-featured management suite for monitoring user registrations, verifying bKash payments, and managing the question repository.

### 🎨 Premium UI/UX
- **Modern Adaptive Design:** Built with **Next.js 14** and **Tailwind CSS**, featuring dark mode, glassmorphism, and smooth micro-animations for a premium feel.
- **Mobile Responsive:** Optimized for both mobile devices and desktop workstations to support "on-the-go" practice.

---

## 🛠 Tech Stack

### Frontend
- **Framework:** [Next.js 14](https://nextjs.org/) (App Router)
- **Language:** TypeScript
- **State Management:** [Zustand](https://github.com/pmndrs/zustand)
- **Styling:** Tailwind CSS & Framer Motion
- **Form Handling:** React Hook Form & Zod

### Backend
- **Framework:** [Django REST Framework](https://www.django-rest-framework.org/)
- **Core:** Django 5.x
- **Database:** PostgreSQL
- **Static File Handling:** WhiteNoise
- **WSGI Server:** Gunicorn

### Infrastructure & DevOps
- **Deployment:** Render (Backend) & Vercel (Frontend)
- **Containerization:** Docker & Docker Compose
- **Configuration:** Infrastructure as Code (render.yaml)
- **Communication:** RESTful API with Axios Interceptors

---

## 🏗️ Technical Architecture

### Device Fingerprinting & Security
To maintain the commercial integrity of the coaching center, the platform implements a `device_fingerprint` system. Upon login, a unique hardware-based identifier is validated and stored. Subsequent logins from different hardware are blocked until the previous session is cleanly terminated, effectively stopping account sharing in a commercial environment.

### Optimized Analytics Engine
Rather than simple database counts, the platform features a `PerformanceAnalytics` engine. It calculates:
- **Average Questions Answered per Test**
- **Score Accuracy Percentages**
- **Total Time-on-Platform Metrics**
The system includes a custom management command to recalculate these metrics globally to ensure data integrity during updates.

---

## ⚙️ Development Setup

### Backend (Django)
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements/development.txt
python manage.py migrate
python manage.py runserver
```

### Frontend (Next.js)
```bash
cd frontend
npm install
npm run dev
```

---

## 📄 License & Proprietary Information
This project is proprietary and was custom-built for **Bangladesh Bravo Academy**. All rights to the logic and question datasets are reserved by the Academy.

---

*Designed and Developed with ❤️ for the future officers of the Bangladesh Armed Forces.*
