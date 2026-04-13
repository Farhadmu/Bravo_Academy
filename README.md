# Bravo Academy Platform

<div align="center">

![Version](https://img.shields.io/badge/version-2.1.0-blue.svg?style=for-the-badge)
![Status](https://img.shields.io/badge/status-production-success.svg?style=for-the-badge)
![Stack](https://img.shields.io/badge/stack-Next.js%20%7C%20Django-black.svg?style=for-the-badge)

**A high-performance adaptive testing & online education platform for defense recruitment preparation.**

[Live Site](https://bravoacademy.vercel.app) • [Backend API](https://bravo-academy-backend-fywx.onrender.com) • [Report Bug](mailto:sakiburrahmannnn@gmail.com)

</div>

---

## Table of Contents

- [Overview](#overview)
- [Technical Architecture](#technical-architecture)
- [Repository Structure](#repository-structure)
- [Prerequisites](#prerequisites)
- [Local Development Setup](#local-development-setup)
- [Environment Variables](#environment-variables)
- [Production Deployment](#production-deployment)
- [Database](#database)
- [API Reference](#api-reference)
- [Key Features](#key-features)
- [Contribution Guidelines](#contribution-guidelines)

---

## Overview

**Bravo Academy** is a full-stack ed-tech platform engineered to simulate high-stakes ISSB testing environments. It uses a decoupled headless architecture with **Next.js 16** on the frontend and **Django 5 REST Framework** on the backend.

The platform serves **1,500+ testing assets**, supports multiple test formats (MCQ, True/False, Word Association), and provides real-time performance analytics with category benchmarking.

---

## Technical Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         INTERNET                                │
│                                                                 │
│  ┌──────────────────┐              ┌──────────────────────┐     │
│  │  Vercel (Edge)   │   HTTPS/API  │  Render (Singapore)  │     │
│  │                  │ ────────────►│                      │     │
│  │  Next.js 16      │              │  Django 5.1 + DRF    │     │
│  │  React 19        │◄──────────── │  Gunicorn WSGI       │     │
│  │  Tailwind CSS    │   JSON/JWT   │  WhiteNoise Static   │     │
│  └──────────────────┘              └──────────┬───────────┘     │
│                                               │                 │
│                                    ┌──────────▼───────────┐     │
│                                    │  Supabase (AWS       │     │
│                                    │  ap-south-1)         │     │
│                                    │                      │     │
│                                    │  PostgreSQL 15       │     │
│                                    │  S3 Media Storage    │     │
│                                    └──────────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
```

### Core Stack

| Layer | Technology | Details |
| :--- | :--- | :--- |
| **Frontend** | Next.js 16 (React 19) | App Router, Server Actions, Tailwind CSS, Radix UI, Zustand |
| **Backend** | Django 5.1, DRF | ViewSets, Serializers, Signals, Cookie-based JWT Auth |
| **Database** | PostgreSQL 15 (Supabase) | Connection pooling via Supavisor, SSL enforced |
| **Storage** | S3-compatible (Supabase) | `django-storages` + `boto3` for media delivery |
| **Auth** | SimpleJWT (Cookie-based) | HttpOnly cookies, SameSite=None (cross-origin), PBKDF2 hashing |

---

## Repository Structure

```
Bravo_Academy/
├── backend/                        # Django REST API
│   ├── apps/
│   │   ├── users/                  # Authentication, profiles, device fingerprinting
│   │   ├── tests/                  # Test engine, session management, timing logic
│   │   ├── questions/              # Question bank, S3 media linking
│   │   └── results/                # Scoring algorithms, analytics, history
│   ├── config/
│   │   ├── settings/
│   │   │   ├── base.py             # Shared settings (INSTALLED_APPS, middleware, JWT)
│   │   │   ├── development.py      # Local dev overrides (DEBUG=True, SQLite fallback)
│   │   │   └── production.py       # Production hardening (SSL, CSP, S3, Supabase)
│   │   ├── urls.py                 # Root URL configuration
│   │   └── wsgi.py                 # WSGI entry point
│   ├── scripts/
│   │   └── render_build.sh         # Render build automation script
│   ├── requirements.txt            # Python dependencies (production)
│   ├── requirements/
│   │   └── development.txt         # Dev-only dependencies (debug toolbar, etc.)
│   ├── manage.py
│   └── .env.example                # Backend environment template
│
├── frontend/                       # Next.js 16 Application
│   ├── src/
│   │   ├── app/
│   │   │   ├── (auth)/             # Login, registration, password reset pages
│   │   │   ├── (dashboard)/        # Student dashboard, test-taking, results
│   │   │   ├── (developer)/        # Admin/developer panel
│   │   │   ├── (public)/           # Public landing pages
│   │   │   ├── layout.tsx          # Root layout
│   │   │   └── page.tsx            # Landing page
│   │   ├── components/             # Reusable UI components (Shadcn/Radix)
│   │   └── lib/                    # API client, auth helpers, utilities
│   ├── package.json
│   └── .env.example                # Frontend environment template
│
├── docker/                         # Dockerfiles for backend and frontend
├── docker-compose.yml              # Full-stack local development via Docker
├── render.yaml                     # Render IaC deployment configuration
└── README.md
```

---

## Prerequisites

| Tool | Version | Purpose |
| :--- | :--- | :--- |
| **Python** | 3.12+ | Backend runtime |
| **Node.js** | 20+ | Frontend runtime |
| **PostgreSQL** | 15+ | Database (or use Docker) |
| **Docker** *(optional)* | 24+ | Containerized local development |

---

## Local Development Setup

### Option A: Manual Setup

#### 1. Clone the Repository

```bash
git clone git@github.com:Farhadmu/Bravo_Academy.git
cd Bravo_Academy
```

#### 2. Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your local database credentials

# Run migrations and start server
python manage.py migrate
python manage.py runserver
```

The API will be available at `http://localhost:8000`.

#### 3. Frontend

```bash
cd frontend
npm install

# Configure environment
cp .env.example .env.local
# Edit .env.local — set NEXT_PUBLIC_API_URL=http://localhost:8000

npm run dev
```

The frontend will be available at `http://localhost:3000`.

### Option B: Docker (Recommended)

```bash
# From root directory
cp backend/.env.example backend/.env
# Edit backend/.env with your desired database credentials

docker compose up --build
```

This starts PostgreSQL, pgAdmin, backend, and frontend simultaneously.

| Service | URL |
| :--- | :--- |
| Frontend | `http://localhost:3000` |
| Backend API | `http://localhost:8000` |
| pgAdmin | `http://localhost:5050` |

---

## Environment Variables

### Backend (`backend/.env`)

| Variable | Required | Description | Example |
| :--- | :---: | :--- | :--- |
| `DATABASE_URL` | ✅ | PostgreSQL connection string | `postgresql://user:pass@host:5432/dbname` |
| `SECRET_KEY` | ✅ | Django secret key | Random 50+ char string |
| `DEBUG` | ✅ | Debug mode | `True` (local) / `False` (prod) |
| `DJANGO_SETTINGS_MODULE` | ✅ | Settings module path | `config.settings.production` |
| `ALLOWED_HOSTS` | ✅ | Comma-separated allowed hosts | `localhost,127.0.0.1` |
| `CORS_ALLOWED_ORIGINS` | ✅ | Comma-separated CORS origins | `http://localhost:3000` |
| `PYTHON_VERSION` | ⬚ | Python version (Render) | `3.12.3` |
| `JWT_ACCESS_TOKEN_LIFETIME` | ⬚ | Access token TTL (minutes) | `60` |
| `JWT_REFRESH_TOKEN_LIFETIME` | ⬚ | Refresh token TTL (minutes) | `10080` |
| `AWS_ACCESS_KEY_ID` | ⬚ | S3-compatible storage key | Supabase S3 access key |
| `AWS_SECRET_ACCESS_KEY` | ⬚ | S3-compatible storage secret | Supabase S3 secret key |
| `AWS_S3_ENDPOINT_URL` | ⬚ | S3 endpoint URL | `https://<project>.storage.supabase.co/storage/v1/s3` |
| `AWS_STORAGE_BUCKET_NAME` | ⬚ | S3 bucket name | `media` |
| `PGSSLMODE` | ⬚ | PostgreSQL SSL mode | `require` |

### Frontend (`frontend/.env.local`)

| Variable | Required | Description | Example |
| :--- | :---: | :--- | :--- |
| `NEXT_PUBLIC_API_URL` | ✅ | Backend API base URL | `http://localhost:8000` |
| `NEXT_PUBLIC_SITE_URL` | ✅ | Frontend public URL | `http://localhost:3000` |

---

## Production Deployment

### Current Infrastructure

| Service | Platform | Region | URL |
| :--- | :--- | :--- | :--- |
| **Frontend** | Vercel | Edge (Global) | [bravoacademy.vercel.app](https://bravoacademy.vercel.app) |
| **Backend** | Render (Free) | Singapore | [bravo-academy-backend-fywx.onrender.com](https://bravo-academy-backend-fywx.onrender.com) |
| **Database** | Supabase | AWS ap-south-1 | Session Pooler on port 5432 |

### Deploying Backend to Render

1. Create a new **Web Service** on [Render](https://render.com).
2. Connect the GitHub repository `Farhadmu/Bravo_Academy`.
3. Configure:
   - **Root Directory:** `backend`
   - **Runtime:** Python
   - **Build Command:** `pip install --upgrade pip && pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate --no-input`
   - **Start Command:** `gunicorn config.wsgi:application --bind=0.0.0.0:$PORT --timeout=180 --workers=1 --threads=4 --worker-class=gthread`
4. Set all required environment variables from the table above.

> **⚠️ Important:** When connecting to Supabase from Render, use the **Session Pooler** connection string (IPv4), NOT the Direct Connection (IPv6). Render does not support IPv6.
>
> Format: `postgresql://postgres.<project_ref>:<password>@aws-1-ap-south-1.pooler.supabase.com:5432/postgres?sslmode=require`

### Deploying Frontend to Vercel

1. Import the repository on [Vercel](https://vercel.com).
2. Set **Root Directory** to `frontend`.
3. Vercel auto-detects Next.js. Set environment variables:
   - `NEXT_PUBLIC_API_URL` → Your Render backend URL (e.g., `https://bravo-academy-backend-fywx.onrender.com`)
   - `NEXT_PUBLIC_SITE_URL` → Your Vercel domain (e.g., `https://bravoacademy.vercel.app`)
4. Deploy.

### Render Free Tier Note

The Render free tier spins down after 15 minutes of inactivity. The first request after spin-down will take ~50 seconds. For consistent availability, upgrade to a paid plan or set up an external ping service.

---

## Database

### Schema Overview

The database contains four Django apps:

| App | Tables | Description |
| :--- | :--- | :--- |
| `users` | `User`, `DeviceFingerprint` | Custom user model with role-based access, device tracking |
| `tests` | `Test`, `TestSession`, `TestAttempt` | Test definitions, active sessions, timing logic |
| `questions` | `Question`, `QuestionOption`, `QuestionMedia` | Question bank with S3-linked media assets |
| `results` | `Result`, `ResultDetail`, `ScoreHistory` | Scoring, per-question analytics, longitudinal tracking |

### Running Migrations

```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

### Creating a Superuser

```bash
python manage.py createsuperuser
```

Access the admin panel at `http://localhost:8000/admin/`.

---

## API Reference

The backend exposes a REST API documented via **drf-spectacular** (OpenAPI 3.0).

### Key Endpoints

| Method | Endpoint | Auth | Description |
| :--- | :--- | :---: | :--- |
| `POST` | `/api/auth/register` | ❌ | User registration |
| `POST` | `/api/auth/login` | ❌ | Login (returns JWT cookies) |
| `POST` | `/api/auth/logout` | ✅ | Logout (blacklists refresh token) |
| `POST` | `/api/auth/token/refresh` | ✅ | Refresh access token |
| `GET` | `/api/tests/` | ✅ | List available tests |
| `POST` | `/api/tests/{id}/start` | ✅ | Start a test session |
| `POST` | `/api/tests/{id}/submit` | ✅ | Submit answers |
| `GET` | `/api/results/` | ✅ | Get user's result history |
| `GET` | `/api/results/{id}/` | ✅ | Get detailed result breakdown |

### Authentication Flow

1. User logs in → Backend sets `access_token` and `refresh_token` as **HttpOnly cookies**.
2. Frontend sends requests with `credentials: 'include'` → Cookies are attached automatically.
3. On 401, frontend calls `/api/auth/token/refresh` → New access token is issued.
4. On logout, refresh token is blacklisted server-side.

---

## Key Features

### Adaptive Testing Engine
- Multi-format support: MCQ, True/False, Word Association Tests (WAT)
- Server-authoritative timing to prevent client-side manipulation
- Auto-resume on interrupted sessions with precise state restoration

### Performance Analytics
- Per-question time vs. accuracy scatter plots
- Category benchmarking (Verbal, Non-Verbal, Abstract Reasoning)
- Longitudinal performance tracking via Recharts

### Admin Panel
- User lifecycle management (CRUD, ban, role assignment)
- Dynamic question bank with bulk upload and S3 media linking
- Payment verification workflow for premium test access

### Security
- Strict Content Security Policy (CSP)
- Role-Based Access Control (Student, Admin, Developer)
- Device fingerprinting for session integrity
- Rate limiting on all authentication endpoints

---

## Contribution Guidelines

1. **Branching:** Use short-lived feature branches off `main`.
2. **Commits:** Follow [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `chore:`, etc.).
3. **Code Style:**
   - Python: Follow PEP 8. Use type hints.
   - TypeScript: Follow ESLint + Prettier configuration in the project.
4. **Testing:** Write tests for new features. Run existing tests before opening a PR.
5. **PRs:** Target `main`. Include a description of changes and any migration steps.

---

## License

This project is proprietary. All rights reserved.

---

<div align="center">

**Built by [Sakibur Rahman](mailto:sakiburrahmannnn@gmail.com)**

</div>
