# 🎯 Bravo Academy - ISSB Preparation Platform

[![Django](https://img.shields.io/badge/Django-5.x-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Next.js](https://img.shields.io/badge/Next.js-16-000000?logo=next.js&logoColor=white)](https://nextjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Latest-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)]()

> **Professional IQ Test Platform for Bangladesh Armed Forces ISSB Exam Preparation**

A production-grade, enterprise-level online education platform designed specifically for Bangladesh Bravo Academy to prepare candidates for the Inter Services Selection Board (ISSB) examinations of the Bangladesh Armed Forces (Army, Navy, Air Force).

## 📖 Overview

Bravo Academy provides a comprehensive, high-pressure testing environment that accurately simulates the real ISSB examination conditions. The platform features timed IQ tests, Word Association Tests (WAT), detailed performance analytics, and a robust payment verification system integrated with Bangladesh's bKash payment gateway.

### Key Statistics
- **15 Test Sets**: 10 Standard IQ Tests + 5 Word Association Tests
- **1000+ Questions**: Professionally curated MCQ and True/False questions
- **400 WAT Words**: Specialized word association practice
- **Real-time Analytics**: Comprehensive performance tracking and trend analysis
- **Device-Locked Security**: Advanced fingerprinting to prevent account sharing

---

## ✨ Core Features

### 🧠 Advanced Testing Engine
- ✅ **Authentic ISSB Simulation**: 100 questions in 30 minutes with strict auto-submission
- ✅ **Multiple Question Types**: Multiple Choice Questions (MCQ), True/False, and Word Association Tests (WAT)
- ✅ **Server-Side Timer**: Robust timezone-independent timer calculation
- ✅ **Auto-Save Answers**: Real-time answer persistence to prevent data loss
- ✅ **Image Support**: High-quality diagrams and visual questions stored in Supabase
- ✅ **Question Navigator**: Quick jump navigation with visual progress indicators

### 🛡️ Enterprise Security
- ✅ **Device Fingerprinting**: One-device-per-user restriction to prevent commercial account sharing
- ✅ **JWT Authentication**: Short-lived access tokens with secure refresh mechanism
- ✅ **Argon2 Hashing**: Military-grade password encryption (Password Hashing Competition winner)
- ✅ **CORS Protection**: Whitelist-based cross-origin resource sharing
- ✅ **IP Tracking**: Login history and device change monitoring

### 📊 Performance Analytics Engine
- ✅ **Comprehensive Metrics**: Average score, accuracy, time spent, questions answered
- ✅ **Trend Analysis**: Score progression and performance visualization with Recharts
- ✅ **Test History**: Complete record of all attempts with detailed breakdowns
- ✅ **Accuracy Calculation**: Quality-based metrics (correct/answered, not correct/total)
- ✅ **WAT Exclusion**: Word Association Tests don't affect performance statistics

### 💳 Payment Management System
- ✅ **bKash Integration**: Manual verification workflow for Bangladeshi payments
- ✅ **Screenshot Verification**: Admin review of payment proofs
- ✅ **User Access Control**: Granular test access grants post-verification
- ✅ **Transaction Tracking**: Complete payment history with status management

### 🎨 Modern UI/UX
- ✅ **Next.js 16 App Router**: Server Components and optimized routing
- ✅ **Responsive Design**: Mobile-first approach with Tailwind CSS
- ✅ **Dark Mode Support**: System preference detection
- ✅ **Accessibility**: WCAG 2.1 AA compliant with Radix UI primitives
- ✅ **Professional Animations**: Smooth transitions and micro-interactions

---

## 🏗️ Architecture

### System Design

```
┌─────────────────────────────────────────────────────────────┐
│                     Client Layer                             │
│  Next.js 16 (TypeScript) + Tailwind CSS + Zustand          │
└────────────────────┬────────────────────────────────────────┘
                     │ REST API (JSON)
                     │ JWT Authentication
┌────────────────────▼────────────────────────────────────────┐
│                   API Gateway Layer                          │
│         Django REST Framework + CORS + JWT                   │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┬──────────────┐
        │            │            │              │
┌───────▼──────┐ ┌──▼─────┐ ┌───▼──────┐ ┌────▼──────┐
│   Users      │ │ Tests  │ │Questions │ │ Results   │
│   App        │ │  App   │ │   App    │ │   App     │
└──────────────┘ └────────┘ └──────────┘ └───────────┘
        │            │            │              │
        └────────────┴────────────┴──────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                PostgreSQL Database                           │
│         (Supabase Managed + Connection Pooling)             │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

#### Backend
| Layer | Technology | Purpose |
|-------|-----------|---------|
| Framework | Django 5.x | Core application logic |
| API | Django REST Framework | RESTful API endpoints |
| Database | PostgreSQL | Primary data store |
| ORM | Django ORM | Database abstraction |
| Auth | Simple JWT | Token-based authentication |
| Password | Argon2 | Secure password hashing |
| Server | Gunicorn | Production WSGI server |
| Static Files | WhiteNoise | Static asset serving |
| Media Storage | Supabase Storage | S3-compatible image storage |

#### Frontend
| Layer | Technology | Purpose |
|-------|-----------|---------|
| Framework | Next.js 16 | React meta-framework |
| Language | TypeScript 5.x | Type-safe JavaScript |
| UI Library | React 19 | Component framework |
| Styling | Tailwind CSS 3.4 | Utility-first CSS |
| Components | Radix UI | Accessible primitives |
| State | Zustand 5.0 | Lightweight state management |
| Forms | React Hook Form + Zod | Form handling + validation |
| HTTP | Axios | API communication |
| Charts | Recharts | Data visualization |
| Icons | Lucide React | Modern icon library |

#### DevOps & Infrastructure
| Component | Platform | Purpose |
|-----------|----------|---------|
| Backend Hosting | Render | Managed Django deployment |
| Frontend Hosting | Vercel | Edge-optimized Next.js |
| Database | Supabase | Managed PostgreSQL |
| Media Storage | Supabase Storage | Image CDN |
| CI/CD | GitHub Actions | Automated deployments |
| Monitoring | Render Logs | Application monitoring |

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.11+** (Backend)
- **Node.js 18+** & npm (Frontend)
- **PostgreSQL 14+** (Database)
- **Git** (Version control)

### Environment Setup

#### 1. Clone Repository
```bash
git clone https://github.com/SakiburRahmann/Online-Education-Platform.git
cd Online-Education-Platform
```

#### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements/development.txt

# Create .env file
cp .env.example .env
# Edit .env with your database credentials

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load sample data (optional)
python scripts/seed_wat_set1.py

# Run development server
python manage.py runserver
```

Backend will be available at `http://localhost:8000`

#### 3. Frontend Setup

```bash
# Navigate to frontend directory (from project root)
cd frontend

# Install dependencies
npm install

# Create .env.local file
cp .env.example .env.local
# Edit .env.local:
# NEXT_PUBLIC_API_URL=http://localhost:8000/api

# Run development server
npm run dev
```

Frontend will be available at `http://localhost:3000`

---

## 📁 Project Structure

```
online-edu/
├── backend/                      # Django REST API
│   ├── apps/                     # Modular Django applications
│   │   ├── users/                # Authentication & user management
│   │   │   ├── models.py         # Custom User model with device tracking
│   │   │   ├── views.py          # Auth endpoints (login, register, token refresh)
│   │   │   └── serializers.py    # User data serialization
│   │   ├── tests/                # Test & session management
│   │   │   ├── models.py         # Test, TestSession models
│   │   │   ├── views.py          # Test CRUD, start_test, submit endpoints
│   │   │   └── serializers.py    # Test data + remaining_seconds calculation
│   │   ├── questions/            # Question management
│   │   │   ├── models.py         # Question, QuestionImage models
│   │   │   └── admin.py          # Admin interface for questions
│   │   ├── results/              # Results & analytics
│   │   │   ├── models.py         # Result, PerformanceAnalytics models
│   │   │   └── views.py          # Result retrieval endpoints
│   │   └── payments/             # Payment verification
│   │       ├── models.py         # Payment, UserTestAccess models
│   │       └── admin.py          # Admin payment approval interface
│   ├── config/                   # Django configuration
│   │   ├── settings/             # Environment-specific settings
│   │   │   ├── base.py           # Shared settings
│   │   │   ├── development.py   # Local development
│   │   │   └── production.py    # Production settings
│   │   ├── urls.py               # API routing
│   │   └── wsgi.py               # WSGI application
│   ├── scripts/                  # Data management scripts
│   │   ├── seed_wat_set1.py      # WAT Set 1 (80 words)
│   │   ├── seed_wat_set2.py      # WAT Set 2 (80 words)
│   │   ├── seed_wat_set3.py      # WAT Set 3 (80 words)
│   │   ├── seed_wat_set4.py      # WAT Set 4 (80 words)
│   │   ├── seed_wat_set5.py      # WAT Set 5 (80 words)
│   │   ├── seed_questions.py     # IQ Test Set 1 (100 questions)
│   │   └── seed_set2-10_complete.py  # IQ Test Sets 2-10
│   ├── utils/                    # Utility modules
│   │   └── device_tracking.py    # Device fingerprint validation
│   ├── manage.py                 # Django management script
│   └── requirements.txt          # Python dependencies
│
├── frontend/                     # Next.js Application
│   ├── src/
│   │   ├── app/                  # Next.js 14 App Router
│   │   │   ├── (public)/         # Public pages (no auth)
│   │   │   │   ├── page.tsx      # Landing page
│   │   │   │   ├── about/        # About Bravo Academy
│   │   │   │   └── contact/      # Contact information
│   │   │   ├── (auth)/           # Authentication pages
│   │   │   │   ├── login/        # User login
│   │   │   │   └── register/     # User registration
│   │   │   └── (dashboard)/      # Protected pages
│   │   │       ├── dashboard/    # Student portal
│   │   │       │   ├── page.tsx  # Dashboard home
│   │   │       │   ├── tests/[id]/page.tsx      # Test runner
│   │   │       │   └── results/[id]/page.tsx    # Result viewer
│   │   │       └── admin/        # Admin portal
│   │   │           ├── payments/ # Payment verification
│   │   │           ├── tests/    # Test management
│   │   │           └── users/    # User management
│   │   ├── components/           # React components
│   │   │   ├── ui/               # Reusable UI components (Button, Card, etc.)
│   │   │   ├── layout/           # Layout components (Navbar, Footer)
│   │   │   └── common/           # Common utilities (BackendWakeupManager)
│   │   └── lib/                  # Utilities & configurations
│   │       ├── api.ts            # Axios instance with interceptors
│   │       ├── fingerprint.ts    # Device fingerprinting
│   │       └── utils.ts          # Helper functions
│   ├── public/                   # Static assets
│   ├── package.json              # npm dependencies
│   └── tailwind.config.ts        # Tailwind CSS configuration
│
├── docker/                       # Docker configuration (optional)
├── docs/                         # Documentation
├── .gitignore                    # Git ignore rules
├── docker-compose.yml            # Local development stack
├── render.yaml                   # Render deployment configuration
└── README.md                     # This file
```

---

## 🔐 Security Features

### Device Fingerprinting System

**Purpose**: Prevent commercial account sharing by restricting each student account to a single device.

**Implementation**:
1. **Frontend**: Uses FingerprintJS library to generate unique hardware-based identifier
2. **Backend**: Stores fingerprint in `User.device_fingerprint` field
3. **Enforcement**: `can_login_from_device()` method validates on every login
4. **Admin Bypass**: Admin users can log in from any device for support purposes

**Code Reference**:
```python
# backend/apps/users/models.py
def can_login_from_device(self, fingerprint):
    if self.role == 'admin' or self.is_superuser:
        return True  # Admins unrestricted
    if not self.device_fingerprint:
        return True  # First login
    return self.device_fingerprint == fingerprint
```

### Authentication Flow

```
1. User Login
   ↓
2. Device Fingerprint Generated (Frontend)
   ↓
3. Fingerprint Sent with Credentials
   ↓
4. Backend Validates Device
   ↓
5. JWT Tokens Issued (Access + Refresh)
   ↓
6. Tokens Stored in localStorage
   ↓
7. Auto-refresh on 401 Response
```

### Password Security
- **Hashing Algorithm**: Argon2 (OWASP recommended)
- **Salt**: Automatically generated per user
- **Iterations**: Configured for optimal security/performance balance
- **No Plain Text**: Passwords never stored or logged in plain text

---

## 📊 Database Schema

### Core Models

#### User Model
```python
class User(AbstractBaseUser, PermissionsMixin):
    id = UUIDField(primary_key=True)
    username = CharField(unique=True)
    role = CharField(choices=['admin', 'student', 'staff'])
    full_name = CharField()
    phone = CharField()
    device_fingerprint = CharField()  # Hardware ID
    last_login_ip = GenericIPAddressField()
    is_active = BooleanField(default=True)
```

#### Test Model
```python
class Test(Model):
    id = UUIDField(primary_key=True)
    name = CharField()
    duration_minutes = IntegerField(default=30)
    total_questions = IntegerField(default=100)
    price = DecimalField()
    passing_score = IntegerField(default=50)
    is_free_sample = BooleanField()
    is_bank = BooleanField()  # Unified question bank
```

#### TestSession Model
```python
class TestSession(Model):
    id = UUIDField(primary_key=True)
    user = ForeignKey(User)
    test = ForeignKey(Test)
    status = CharField(choices=['in_progress', 'completed', 'expired'])
    answers = JSONField()  # {"question_id": "option_id"}
    score = IntegerField()
    percentage = DecimalField()
    time_spent_seconds = IntegerField()
```

#### Question Model
```python
class Question(Model):
    id = UUIDField(primary_key=True)
    test = ForeignKey(Test)
    question_text = TextField()
    question_type = CharField(choices=['mcq', 'true_false', 'wat'])
    options = JSONField()  # [{"id": "a", "text": "..."}]
    correct_answer = CharField()
    difficulty_level = CharField(choices=['easy', 'medium', 'hard'])
```

#### Result Model
```python
class Result(Model):
    id = UUIDField(primary_key=True)
    user = ForeignKey(User)
    test_session = OneToOneField(TestSession)
    correct_answers = IntegerField()
    wrong_answers = IntegerField()
    unanswered = IntegerField()
    accuracy = DecimalField()  # Correct / Answered * 100
```

#### PerformanceAnalytics Model
```python
class PerformanceAnalytics(Model):
    id = UUIDField(primary_key=True)
    user = OneToOneField(User)
    total_tests_taken = IntegerField()
    average_score = DecimalField()
    average_accuracy = DecimalField()
    highest_score = DecimalField()
    total_time_spent = IntegerField()
```

---

## 🎯 API Documentation

### Base URL
- **Development**: `http://localhost:8000/api`
- **Production**: `https://online-education-platform-tdc4.onrender.com/api`

### Authentication Endpoints

#### Register
```http
POST /users/register/
Content-Type: application/json

{
  "username": "student1",
  "password": "SecurePass123!",
  "full_name": "John Doe",
  "phone": "01712345678"
}
```

#### Login
```http
POST /users/login/
Content-Type: application/json
X-Device-Fingerprint: <fingerprint_hash>

{
  "username": "student1",
  "password": "SecurePass123!"
}
```

**Response**:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": "uuid",
    "username": "student1",
    "role": "student"
  }
}
```

### Test Endpoints

#### List Tests
```http
GET /tests/tests/
Authorization: Bearer <access_token>
```

#### Start Test (Optimized)
```http
POST /tests/tests/{test_id}/start_test/
Authorization: Bearer <access_token>
```

**Response** (Single API call returns everything):
```json
{
  "test": {...},
  "session": {
    "id": "uuid",
    "remaining_seconds": 1784
  },
  "questions": [...]
}
```

#### Save Answers (Auto-save)
```http
PATCH /tests/test-sessions/{session_id}/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "answers": {
    "question_uuid_1": "option_a",
    "question_uuid_2": "option_c"
  }
}
```

#### Submit Test
```http
POST /tests/test-sessions/{session_id}/submit/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "answers": {...}
}
```

### Result Endpoints

#### Get Result
```http
GET /results/results/{result_id}/
Authorization: Bearer <access_token>
```

**Response**:
```json
{
  "id": "uuid",
  "test_name": "IQ Test Set 1",
  "question_type": "mcq",
  "correct_answers": 75,
  "wrong_answers": 20,
  "unanswered": 5,
  "score_percentage": 75.00,
  "accuracy": 78.95,
  "time_taken_seconds": 1680,
  "review_data": [...]
}
```

---

## 🧪 Testing

### Backend Tests
```bash
cd backend
python manage.py test
```

### Frontend Tests
```bash
cd frontend
npm run test
```

### Data Validation
```bash
# Verify question integrity
python backend/scripts/validate_set1_jumbles.py

# Verify WAT sets
python backend/scripts/verify_wat.py
```

---

## 🚢 Deployment

### Production Architecture

```
User → Vercel (Frontend) → Render (Backend) → Supabase (Database)
                                          ↓
                                  Supabase Storage (Images)
```

### Backend Deployment (Render)

**Configuration**: `render.yaml`
```yaml
services:
  - type: web
    name: online-edu-backend
    env: python
    buildCommand: pip install -r requirements.txt && python manage.py migrate
    startCommand: gunicorn config.wsgi:application
```

**Environment Variables**:
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: Django secret key
- `CORS_ALLOWED_ORIGINS`: Frontend URL
- `SUPABASE_URL`: Supabase project URL
- `SUPABASE_KEY`: Supabase API key

### Frontend Deployment (Vercel)

**Configuration**: Automatic via `vercel.json`

**Environment Variables**:
- `NEXT_PUBLIC_API_URL`: Backend API URL

### Database (Supabase)

**Connection String Format**:
```
postgresql://postgres.[PROJECT_ID]:[PASSWORD]@aws-1-ap-south-1.pooler.supabase.com:6543/postgres
```

**Features**:
- Connection pooling enabled
- Automatic backups
- Point-in-time recovery
- Public storage bucket for images

---

## 📝 Usage Guide

### For Students

1. **Registration**:
   - Send bKash payment (1000 TK) to `01979486096`
   - WhatsApp payment screenshot to admin
   - Wait for account creation

2. **Taking Tests**:
   - Log in with provided credentials
   - Browse available tests
   - Click "Start Test" to begin
   - Submit before timer expires
   - Review detailed results

3. **Viewing Analytics**:
   - Dashboard shows comprehensive performance metrics
   - Track score trends over time
   - Identify weak areas

### For Admins

1. **Payment Verification**:
   - Navigate to `/admin/payments/payment/`
   - Review pending payments
   - Verify transaction IDs and screenshots
   - Approve or reject payments

2. **User Management**:
   - Create user accounts post-payment
   - Grant test access via `UserTestAccess`
   - Monitor user activity

3. **Test Management**:
   - Create new tests via Django Admin
   - Run seeding scripts to populate questions
   - Monitor test sessions

---

## 🛠️ Development Guide

### Code Style

**Backend (Python)**:
- Follow PEP 8 guidelines
- Use Django conventions
- Type hints encouraged
- Docstrings for all public methods

**Frontend (TypeScript)**:
- ESLint configuration enforced
- Prettier for formatting
- Functional components with hooks
- Type everything

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "feat: add new feature"

# Push to remote
git push origin feature/new-feature

# Create pull request on GitHub
```

### Database Migrations

```bash
# Create migration after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Rollback migration
python manage.py migrate app_name previous_migration_name
```

---

## 🤝 Contributing

This is a proprietary project for **Bravo Academy**. External contributions are not accepted at this time.

For internal team members:
1. Fork the repository
2. Create a feature branch
3. Make your changes with proper tests
4. Submit a pull request for review
5. Wait for approval from project lead

---

## 📄 License

**Proprietary and Confidential**

This project and all associated code, designs, and question databases are the exclusive property of **Bangladesh Bravo Academy**. All rights reserved.

Unauthorized copying, distribution, modification, or use of this software in whole or in part is strictly prohibited and may result in severe civil and criminal penalties.

---

## 👥 Team

**Project Lead**: Bravo Academy Technical Team  
**Backend Architecture**: Django REST Framework  
**Frontend Development**: Next.js & TypeScript  
**Database Design**: PostgreSQL with Supabase  
**DevOps**: Render + Vercel Deployment  

---

## 📞 Support

**For Students**:
- WhatsApp: `+880 1979486096`
- Email: Available upon registration

**For Technical Issues**:
- Create an issue in the internal repository
- Contact system administrator

---

## 🎓 Acknowledgments

Built with dedication for the future officers of the Bangladesh Armed Forces.

**Technologies**: Django • Next.js • PostgreSQL • TypeScript • Tailwind CSS • Vercel • Render • Supabase

**Special Thanks**: All contributors to the open-source libraries that made this platform possible.

---

<div align="center">

**Bravo Academy** - Excellence in ISSB Preparation

*Preparing tomorrow's leaders today* 🇧🇩

</div>
