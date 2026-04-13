# Bravo Academy Platform

<div align="center">

![Version](https://img.shields.io/badge/version-2.1.0-blue.svg?style=for-the-badge)
![Stack](https://img.shields.io/badge/stack-Next.js%20%7C%20Django-black.svg?style=for-the-badge)

**Adaptive testing & online education platform for defense recruitment preparation.**

</div>

---

## Overview

Bravo Academy is a full-stack ed-tech platform that simulates ISSB testing environments. It supports multiple test formats (MCQ, True/False, Word Association), real-time performance analytics, and category benchmarking across 1,500+ testing assets.

### Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend** | Next.js 16, React 19, Tailwind CSS, Radix UI, Zustand |
| **Backend** | Django 5.1, Django REST Framework, SimpleJWT |
| **Database** | PostgreSQL 15 |
| **Storage** | S3-compatible (via `django-storages` + `boto3`) |

---

## Repository Structure

```
Bravo_Academy/
├── backend/                        # Django REST API
│   ├── apps/
│   │   ├── users/                  # Auth, profiles, device fingerprinting
│   │   ├── tests/                  # Test engine, sessions, timing
│   │   ├── questions/              # Question bank, media linking
│   │   └── results/                # Scoring, analytics, history
│   ├── config/
│   │   ├── settings/
│   │   │   ├── base.py             # Shared settings
│   │   │   ├── development.py      # Local dev overrides
│   │   │   └── production.py       # Production hardening
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/                       # Next.js Application
│   ├── src/
│   │   ├── app/
│   │   │   ├── (auth)/             # Login, registration
│   │   │   ├── (dashboard)/        # Student dashboard, tests, results
│   │   │   ├── (developer)/        # Admin panel
│   │   │   └── (public)/           # Landing pages
│   │   ├── components/             # UI components (Shadcn/Radix)
│   │   └── lib/                    # API client, utilities
│   ├── package.json
│   └── .env.example
│
├── docker/                         # Dockerfiles
├── docker-compose.yml              # Full-stack local dev
└── render.yaml                     # Render deployment config
```

---

## Prerequisites

- **Python** 3.12+
- **Node.js** 20+
- **PostgreSQL** 15+ (or use Docker)
- **Docker** 24+ *(optional, for containerized setup)*

---

## Local Development Setup

### 1. Clone the Repository

```bash
git clone git@github.com:Farhadmu/Bravo_Academy.git
cd Bravo_Academy
```

### 2. Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
```

Edit `backend/.env` and fill in your values:

```env
DEBUG=True
SECRET_KEY=<generate-a-random-key>
DATABASE_URL=postgresql://<user>:<password>@localhost:5432/<dbname>
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000
SITE_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000
```

Then run:

```bash
python manage.py migrate
python manage.py createsuperuser   # Create an admin account
python manage.py runserver
```

Backend runs at **http://localhost:8000**. Admin panel at **http://localhost:8000/admin/**.

### 3. Frontend

```bash
cd frontend
npm install

# Configure environment
cp .env.example .env.local
```

Edit `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SITE_URL=http://localhost:3000
```

Then run:

```bash
npm run dev
```

Frontend runs at **http://localhost:3000**.

### Alternative: Docker Setup

From the project root:

```bash
docker compose up --build
```

This starts PostgreSQL, pgAdmin, backend, and frontend together.

| Service | URL |
| :--- | :--- |
| Frontend | http://localhost:3000 |
| Backend | http://localhost:8000 |
| pgAdmin | http://localhost:5050 |

---

## API Overview

Authentication uses **HttpOnly JWT cookies**. The frontend handles this automatically via `credentials: 'include'`.

| Method | Endpoint | Auth | Description |
| :--- | :--- | :---: | :--- |
| `POST` | `/api/auth/register` | ❌ | Register |
| `POST` | `/api/auth/login` | ❌ | Login (sets JWT cookies) |
| `POST` | `/api/auth/logout` | ✅ | Logout (blacklists token) |
| `POST` | `/api/auth/token/refresh` | ✅ | Refresh access token |
| `GET` | `/api/tests/` | ✅ | List tests |
| `POST` | `/api/tests/{id}/start` | ✅ | Start a test session |
| `POST` | `/api/tests/{id}/submit` | ✅ | Submit answers |
| `GET` | `/api/results/` | ✅ | User result history |

Full API schema available via **drf-spectacular** at `/api/schema/`.

---

## Contribution Guidelines

1. Branch off `main` with short-lived feature branches.
2. Follow [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `chore:`).
3. Python: PEP 8 with type hints. TypeScript: ESLint + Prettier.
4. Run tests before opening a PR.

---

## License

Proprietary. All rights reserved.
