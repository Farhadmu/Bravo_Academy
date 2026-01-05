# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it immediately to the system administrator through official channels.

**Do not** create public GitHub issues for security vulnerabilities.

## Supported Versions

Only the latest production version receives security updates.

## Security Best Practices

### For Developers

1. **Never commit credentials**: Use environment variables for all sensitive data
2. **Review before commit**: Check for accidentally included secrets
3. **Use .gitignore**: Ensure sensitive files are excluded
4. **Rotate compromised credentials**: Immediately rotate any exposed secrets

### For Users

1. **Strong passwords**: Use complex, unique passwords
2. **Device security**: Only log in from trusted devices
3. **Logout properly**: Always log out after sessions
4. **Report suspicious activity**: Contact administrators immediately

## Password Requirements

- Minimum 8 characters
- Must include uppercase and lowercase letters
- Must include numbers
- Special characters recommended

## Authentication

- JWT tokens expire after configured time
- Refresh tokens must be rotated regularly
- Device fingerprinting prevents unauthorized access
- Failed login attempts are monitored
