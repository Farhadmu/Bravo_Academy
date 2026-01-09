# Security Architecture & Defense-in-Depth

This document provides a professional overview of the security architecture implemented for the Online Education Platform. The system follows the principle of **Defense-in-Depth**, utilizing multiple layers of security to protect user data, financial integrity, and system availability.

## 1. Authentication & Session Management
- **Secure Token Storage**: JWT Access and Refresh tokens are stored in `HttpOnly`, `Secure`, and `SameSite=Lax` cookies. This mitigates the risk of Cross-Site Scripting (XSS) attacks by making tokens inaccessible to client-side scripts.
- **CSRF Protection**: Standard Django CSRF protection is enforced for all state-changing requests, with automatic handling by the frontend API layer.
- **Single Device Enforce**: Users are restricted to a single active device session. Multi-device logins are blocked via fingerprinting and database tracking.
- **Secure Logout**: Logout blacklists the refresh token and clears all authentication cookies and device fingerprints.

## 2. Infrastructure Security
- **Content Security Policy (CSP)**: A strict CSP is enforced to restrict the sources of scripts, styles, and data, significantly reducing the attack surface for injection and data theft.
- **HSTS Enforcement**: HTTP Strict Transport Security (HSTS) is enabled with a long duration and preload policy to ensure all communication happens over secure HTTPS.
- **Fail-Safe Secret Management**: The production environment is configured to crash on startup if critical secrets (e.g., `SECRET_KEY`) are missing or insecure, preventing silent misconfigurations.

## 3. Data Integrity & RBAC
- **Strict Role-Based Access Control (RBAC)**: Permissions are enforced at the API level for every endpoint. 
- **Privilege Escalation Protection**: Core user fields like `role` and `is_active` are immutable via standard user profile updates. Only superusers can modify these through the Admin portal or direct database access.
- **Financial Record Integrity**: Payment records are "create and view only" for students. Once a payment is submitted, it cannot be modified or deleted via the student-facing API.
- **Data Isolation**: Multi-tenancy is enforced at the database query level; students can only access their own results, sessions, and payments.

## 4. API Hardening
- **Rate Limiting (Throttling)**: Brute-force protection is implemented on sensitive endpoints (Login, Registration) using DRF's throttling mechanism.
- **Standardized Error Handling**: A universal exception handler ensures that internal system errors or stack traces are never leaked to the client. Responses are sanitized and professional.
- **Input Sanitization**: All incoming data is validated and cleaned through Django Rest Framework's serializers.

## 5. Observability & Auditing
- **Standardized Logging**: All application errors and sensitive actions are logged using the standard Python `logging` module.
- **Developer Monitoring**: A dedicated, read-only monitoring dashboard allows developers to track real-time user activity, login logs, and system health without compromising data integrity.
- **Database Audit Logging**: Critical developer tools, like the database inspector, log all access attempts and actions for accountability.
