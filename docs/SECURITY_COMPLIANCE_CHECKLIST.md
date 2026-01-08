# Security Compliance Checklist (OWASP Top 10)

This checklist serves as the definitive guide to ensuring and maintaining the security posture of the Online Education Platform. As a "Tech Giant" level professional, I have mapped our implementation against the industry-standard **OWASP Top 10 2021**.

## A01:2021-Broken Access Control
- [x] **Enforce RBAC**: Standardized `permission_classes` in every ViewSet.
- [x] **User Isolation**: Every queryset filters by `user=request.user`.
- [x] **Privilege Escalation Prevention**: `role` and `is_active` fields are read-only in public serializers.
- [x] **Single User Session**: Implemented `ENFORCE_SINGLE_DEVICE` to prevent account sharing/hijacking.

## A02:2021-Cryptographic Failures
- [x] **Secure JWT**: Tokens are signed with `HS256` using a secret managed via environment variables.
- [x] **Token Rotation**: `ROTATE_REFRESH_TOKENS: True` ensures refresh tokens are invalidated after use.
- [x] **HSTS Enforcement**: SSL/TLS is enforced with a 1-year preload policy in production.
- [x] **Weak Password Hashing**: Using `Argon2` (the industry's strongest hasher) as the default.

## A03:2021-Injection
- [x] **ORM Usage**: Zero raw SQL in business logic (uses Django ORM with parameterization).
- [x] **SQL Whitelisting**: The Database Inspector uses a strict whitelist of allowed tables.
- [x] **CSP Protection**: Strict Content Security Policy blocks script injections.

## A04:2021-Insecure Design
- [x] **HttpOnly Cookies**: Neutralizes XSS by hiding tokens from JavaScript.
- [x] **Safe Defaults**: All system settings default to the most secure state (e.g., `DEBUG=False`).
- [x] **Fail-Safe Startup**: Application crashes on missing secrets in production.

## A05:2021-Security Misconfiguration
- [x] **Production Settings**: Hardened `production.py` with unique `ALLOWED_HOSTS` and security headers.
- [x] **Error Handling**: Custom exception handler prevents stack traces from leaking to users.
- [x] **Throttling**: Rate limits implemented on all sensitive endpoints (Login, Register).

## A06:2021-Vulnerable and Outdated Components
- [ ] **Dependency Auditing**: Regularly run `npm audit` and `pip-audit`.
- [ ] **SAST (Static Analysis)**: Integrated `Bandit` (Python) and `ESLint Security`.

## A07:2021-Identification and Authentication Failures
- [x] **Login Monitoring**: Failed attempts are logged for audit.
- [x] **Secure Logout**: Cookies and tokens are explicitly cleared and blacklisted.

## A08:2021-Software and Data Integrity Failures
- [x] **Version Locking**: Using `requirements.txt` and `package-lock.json` for deterministic builds.

## A09:2021-Security Logging and Monitoring Failures
- [x] **Centralized Logging**: Standard Python logging with structured formatters.
- [x] **Developer Dashboard**: High-level telemetry for real-time security monitoring.
- [x] **Audit Trails**: DB Inspector logs all administrative access.

## A10:2021-Server-Side Request Forgery (SSRF)
- [x] **Input Validation**: All URLs and user inputs are strictly validated before use.

---

### Verification Workflow for Owners
1. **Weekly**: Run `npm audit` and update frontend dependencies.
2. **Monthly**: Review `LoginLog` for unusual activity in the Developer Portal.
3. **On Deployment**: Verify the **Security Health Check API** returns a "Green" status.
