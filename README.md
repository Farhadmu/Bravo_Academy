# Bravo Academy - ISSB Preparation Platform

Professional IQ Test Platform for Bangladesh Armed Forces ISSB Exam Preparation

## Overview

Bravo Academy is a production-grade online education platform designed for Bangladesh Bravo Academy to prepare candidates for the Inter Services Selection Board (ISSB) examinations of the Bangladesh Armed Forces (Army, Navy, Air Force). The platform provides comprehensive, timed testing environments that simulate real ISSB examination conditions.

### Platform Features

- **15 Test Sets**: 10 Standard IQ Tests + 5 Word Association Tests
- **1000+ Questions**: Professionally curated MCQ and True/False questions
- **Real-time Analytics**: Comprehensive performance tracking
- **Secure Authentication**: Device-locked accounts with JWT tokens
- **Payment Management**: Integrated verification system

## Architecture

### System Design

The platform follows a modern client-server architecture:

- **Frontend**: Next.js 16 with TypeScript, React 19, and Tailwind CSS
- **Backend**: Django 5.x REST API with Django REST Framework
- **Database**: PostgreSQL (managed)
- **Authentication**: JWT-based with refresh tokens
- **Storage**: Supabase Storage for media files

### Technology Stack

#### Backend

- **Framework**: Django 5.x
- **API**: Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: Simple JWT
- **Password Hashing**: Argon2
- **Server**: Gunicorn
- **Static Files**: WhiteNoise

#### Frontend

- **Framework**: Next.js 16 (App Router)
- **Language**: TypeScript 5.x
- **UI Library**: React 19
- **Styling**: Tailwind CSS 3.4
- **Components**: Radix UI
- **State Management**: Zustand 5.0
- **Forms**: React Hook Form with Zod
- **HTTP Client**: Axios
- **Charts**: Recharts

#### Infrastructure

- **Backend Hosting**: Render
- **Frontend Hosting**: Vercel
- **Database**: Supabase (Managed PostgreSQL)
- **Media Storage**: Supabase Storage

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- PostgreSQL 14 or higher
- Git

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements/development.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your configuration

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

The backend will be available at `http://localhost:8000`

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env.local
# Edit .env.local with your API URL

# Run development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Project Structure

```
online-edu/
├── backend/
│   ├── apps/
│   │   ├── users/          # Authentication & user management
│   │   ├── tests/          # Test & session management
│   │   ├── questions/      # Question management
│   │   ├── results/        # Results & analytics
│   │   └── payments/       # Payment verification
│   ├── config/
│   │   └── settings/       # Environment-specific settings
│   ├── scripts/            # Data seeding scripts
│   └── utils/              # Utility modules
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── (public)/   # Public pages
│   │   │   ├── (auth)/     # Authentication pages
│   │   │   └── (dashboard)/ # Protected pages
│   │   ├── components/     # React components
│   │   └── lib/            # Utilities
│   └── public/             # Static assets
└── README.md
```

## Security Features

### Device Fingerprinting

The platform implements device-based authentication to prevent account sharing:

- Each student account is restricted to a single device
- Admin accounts can access from multiple devices
- Device fingerprints are validated on every login
- Hardware-based identification using FingerprintJS

### Authentication

- JWT-based authentication with access and refresh tokens
- Argon2 password hashing (OWASP recommended)
- Automatic token refresh on expiration
- CORS protection with whitelist

### Data Protection

- All sensitive data encrypted in transit (HTTPS)
- Password complexity requirements enforced
- IP address tracking for security auditing
- No plain text credential storage

## Core Features

### Testing Engine

- Timed ISSB simulations (100 questions in 30 minutes)
- Multiple question types: MCQ, True/False, Word Association Tests
- Server-side timer with robust timezone handling
- Auto-save functionality to prevent data loss
- Image support for visual questions

### Analytics System

- Comprehensive performance metrics
- Score progression tracking
- Accuracy calculations
- Time-based analytics
- Difficulty-based breakdowns

### Admin Portal

- User management
- Payment verification
- Test management
- System statistics
- Content management

## API Documentation

### Base URL

- Development: `http://localhost:8000/api`
- Production: Configure via environment variable

### Authentication Endpoints

#### Register
```
POST /users/register/
Content-Type: application/json
```

#### Login
```
POST /users/login/
Content-Type: application/json
X-Device-Fingerprint: <fingerprint>
```

#### Token Refresh
```
POST /users/token/refresh/
Content-Type: application/json
```

### Test Endpoints

#### List Tests
```
GET /tests/tests/
Authorization: Bearer <token>
```

#### Start Test
```
POST /tests/tests/{id}/start_test/
Authorization: Bearer <token>
```

#### Submit Test
```
POST /tests/test-sessions/{id}/submit/
Authorization: Bearer <token>
```

## Environment Variables

### Backend

Required environment variables for backend configuration:

```
DATABASE_URL=postgresql://user:password@host:port/database
SECRET_KEY=your-secret-key
CORS_ALLOWED_ORIGINS=https://yourdomain.com
ALLOWED_HOSTS=yourdomain.com
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key
```

### Frontend

Required environment variables for frontend configuration:

```
NEXT_PUBLIC_API_URL=https://your-backend-url/api
```

## Deployment

### Backend Deployment

The backend is deployed using Render with the provided `render.yaml` configuration.

### Frontend Deployment

The frontend is deployed using Vercel with automatic deployment from the main branch.

### Database

PostgreSQL database is managed via Supabase with connection pooling enabled.

## Testing

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

## Development Guidelines

### Code Style

**Python**
- Follow PEP 8 guidelines
- Use type hints where applicable
- Document all public methods
- Use Django conventions

**TypeScript**
- Follow ESLint configuration
- Use Prettier for formatting
- Type all components and functions
- Use functional components with hooks

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/description

# Make changes and commit
git add .
git commit -m "type: description"

# Push to remote
git push origin feature/description
```

## Contributing

This is a proprietary project. For internal team members:

1. Create a feature branch
2. Make changes with appropriate tests
3. Submit pull request for review
4. Wait for approval from project lead

## License

**Proprietary and Confidential**

This project and all associated code are the exclusive property of Bangladesh Bravo Academy. All rights reserved.

Unauthorized copying, distribution, modification, or use of this software is strictly prohibited.

## Support

For technical support, please contact the system administrator through official channels.

---

Built for Bangladesh Bravo Academy
