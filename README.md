# Bravo Academy Platform

<div align="center">

![Version](https://img.shields.io/badge/version-2.1.0-blue.svg?style=for-the-badge)
![Status](https://img.shields.io/badge/status-production-success.svg?style=for-the-badge)
![Security](https://img.shields.io/badge/security-hardened-green.svg?style=for-the-badge)
![Stack](https://img.shields.io/badge/stack-Next.js%20%7C%20Django-black.svg?style=for-the-badge)

**A high-performance, enterprise-grade adaptive testing & education platform designed for defense recruitment preparation.**

[Request Access](mailto:admin@example.com) • [Documentation](#) • [Report Bug](#)

</div>

---

## Executive Summary

**Bravo Academy** is a proprietary, full-stack ed-tech solution engineered to simulate high-stakes testing environments (ISSB). Built on a decoupled microservices-ready architecture, it leverages **Next.js 16** for a reactive edge-optimized frontend and **Django 5** for a robust, secure API layer.

The platform distinguishes itself through strict security compliance (HttpOnly JWTs, RBAC, CSP), real-time performance analytics, and a scalable asset management system handling 1,500+ high-fidelity testing assets.

---

## Technical Architecture

The system follows a modern **Headless Architecture**, strictly separating the presentation layer from business logic to ensure scalability and independent deployment cycles.

### Core Stack
| Component | Technology | Key Features |
| :--- | :--- | :--- |
| **Frontend** | **Next.js 16 (React 19)** | App Router, Server Actions, Tailwind CSS, Radix UI, Zustand |
| **Backend** | **Django 5.1 (DRF)** | ViewSets, Serializers, Signals, Gunicorn, WhiteNoise |
| **Database** | **PostgreSQL (Supabase)** | Row Level Security (RLS), Connection Pooling, JSONB Support |
| **Auth** | **JWT (Cookie-Based)** | SimpleJWT, HttpOnly, SameSite=Lax, Argon2 Hashing |
| **Storage** | **S3 Compatible** | Direct-to-cloud media delivery, Secure Presigned URLs |

### Security & Compliance
- **Strict Content Security Policy (CSP)**: Mitigates XSS by verifying all script sources.
- **Role-Based Access Control (RBAC)**: Granular permissions for Student, Admin, and Developer roles.
- **Device Fingerprinting**: Hardware-locked sessions to prevent account sharing.
- **Throttling & Rate Limiting**: Distributed protection against brute-force attacks across all Auth/API endpoints.

---

## Key Features

### Adaptive Testing Engine
- **Multi-Format Support**: Handles MCQ, True/False, and time-critical Word Association Tests (WAT).
- **Latency-Aware Timer**: Server-authoritative timing logic to prevent client-side manipulation.
- **Resilient Sessions**: Auto-resume capability for interrupted tests with precise state restoration.

### Advanced Analytics
- **Performance/Time Correlation**: Detailed scatter plots analyzing time-taken vs. accuracy.
- **Category Benchmarking**: Automatic grading against historical cohort data (Verbal/Non-Verbal/Abstract).
- **History Tracking**: Long-term longitudinal data visualization using `Recharts`.

### Administrative Command Center
- **User Lifecycle Management**: Full CRUD capabilities for user access and ban management.
- **Content CMS**: Dynamic question bank management with bulk-upload and S3 asset linking.
- **Payment Verification**: Manual and automated workflow for premium test access verification.

---

## Repository Structure

```graphql
online-edu/
├── backend/                  # Django REST API
│   ├── apps/
│   │   ├── users/            # Auth, Profiles, Device Fingerprinting
│   │   ├── tests/            # Test Engine & Session Logic
│   │   ├── questions/        # Question Bank & S3 Media
│   │   ├── results/          # Analytics & Scoring Algorithms
│   │   └── system/           # Health Checks & Monitoring
│   ├── config/               # Settings (Base, Dev, Prod)
│   └── scripts/              # Data Seeding & Maintenance automation
├── frontend/                 # Next.js 16 Application
│   ├── src/
│   │   ├── app/              # App Router Pages ((dashboard), (auth))
│   │   ├── components/       # Shadcn/Radix UI Library
│   │   └── lib/              # API Clients & Utilities
├── docker/                   # Containerization Configs
└── docs/                     # Architecture & Security Documentation
```

---

## Deployment Strategy

The infrastructure is designed for high availability and zero-downtime updates.

- **Frontend (Edge)**: Deployed on **Vercel**, leveraging Edge Network for sub-millisecond static asset delivery.
- **Backend (Compute)**: Deployed on **Render**, utilizing auto-scaling workers for API request handling.
- **Data Persistence**: Managed **Supabase** instance with automated daily backups and point-in-time recovery.

---

## Local Development Setup

### Prerequisites
- Python 3.12+
- Node.js 20+
- PostgreSQL 15+

### 1. Backend Initialization
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements/development.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

### 2. Frontend Initialization
```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

---

## Contribution Guidelines

This project adheres to **Enterprise Engineering Standards**.
1. **Trunk-Based Development**: Short-lived feature branches targeting `main`.
2. **Commit Convention**: All commits must follow [Conventional Commits](https://www.conventionalcommits.org/).
3. **Code Quality**: Pre-commit hooks enforce `Black` (Python) and `ESLint/Prettier` (TS) standards.

---

<div align="center">

**Proprietary Software** • Built for **Bravo Academy** • All Rights Reserved

</div>
