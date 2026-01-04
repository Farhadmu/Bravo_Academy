# Bravo Academy Frontend
> **⚠️ PRIVATE CLIENT PROJECT**
> Internal documentation for development and deployment.

A modern, responsive frontend built with Next.js 14, Tailwind CSS, and TypeScript.

## Features

- ⚡ **Next.js 14 App Router** - Server components and advanced routing
- 🎨 **Tailwind CSS** - Utility-first styling with custom design system
- 📝 **TypeScript** - Type-safe development
- 🔐 **Authentication** - JWT integration with role-based protection
- 📱 **Responsive** - Mobile-first design for all devices
- 📊 **Charts** - Data visualization using Recharts

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env.local
   ```
   Update `.env.local` with your backend URL.

3. **Run development server**
   ```bash
   npm run dev
   ```

## Production Build

To successfully build for production:

```bash
npm run build
npm start
```

## Project Structure

- `/src/app` - App router pages and layouts
- `/src/components` - Reusable UI components
- `/src/lib` - Utilities and API configuration
- `/src/store` - Zustand state management
- `/public` - Static assets

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | URL of the backend API | `http://localhost:8000` |
| `NEXT_PUBLIC_SITE_URL` | URL of the frontend site | `http://localhost:3000` |
