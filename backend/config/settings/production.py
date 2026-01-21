"""
Production settings for Defense Coaching Center & IQ Test Platform.
"""
from .base import *

DEBUG = False

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*.onrender.com', cast=Csv())
CSRF_TRUSTED_ORIGINS = [f"https://{host}" for host in ALLOWED_HOSTS if not host.startswith('*')]
if '*.onrender.com' in ALLOWED_HOSTS:
    # This is a bit of a hack because Render doesn't provide the exact hostname as an env var until runtime
    # But usually, you just trust the onrender.com subdomain
    CSRF_TRUSTED_ORIGINS.append("https://*.onrender.com")

# DATABASE CONFIGURATION (Supabase Professional Stability Fixes)
# Using CONN_MAX_AGE=60 to reuse connections and reduce TLS handshake overhead.
# This works for both Direct Connections and Poolers.
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL'),
        conn_max_age=0,
    )
}

# Essential PostgreSQL Options for Supabase (Direct or Pooler)
DATABASES['default']['OPTIONS'] = {
    'sslmode': 'require',
    'connect_timeout': 30,
    # TCP Keepalives to prevent silent connection drops
    'keepalives': 1,
    'keepalives_idle': 30,
    'keepalives_interval': 10,
    'keepalives_count': 5,
}

# Add TCP User Timeout (Linux specific) to drop dead connections faster
import platform
if platform.system() == 'Linux':
    # tcp_user_timeout is in milliseconds (30 seconds)
    DATABASES['default']['OPTIONS']['tcp_user_timeout'] = 30000

# Disable server-side cursors for Supabase Transaction Pooler (PgBouncer/Supavisor) compatibility
# Still beneficial in Session mode for some configurations.
DATABASES['default']['DISABLE_SERVER_SIDE_CURSORS'] = True

# Security settings for production
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_SAMESITE = 'None'
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Content Security Policy (CSP)
# Note: Allows scripts from own domain and inline styles (common for Tailwind/UI libs)
# Adjust these based on external fonts/scripts used (e.g. Google Fonts)
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", "'unsafe-eval'", "https://*.vercel.app")
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", "https://fonts.googleapis.com")
CSP_FONT_SRC = ("'self'", "https://fonts.gstatic.com", "data:")
CSP_IMG_SRC = ("'self'", "data:", "https://*.supabase.co", "https://*.onrender.com")
CSP_CONNECT_SRC = ("'self'", "https://*.supabase.co", "https://*.onrender.com")
CSP_FRAME_ANCESTORS = ("'none'",)

# SECRET_KEY check (Handled by Django, but logging a warning is safer for builds)
if not SECRET_KEY or SECRET_KEY == 'django-insecure-change-this':
    logger.warning("SECRET_KEY is using a default or insecure value in production!")

# WhiteNoise configuration already in base.py
# Static files compression for production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Supabase Storage (S3 Compatible) Configuration
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID', default=None)
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY', default=None)
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME', default='media')
AWS_S3_ENDPOINT_URL = config('AWS_S3_ENDPOINT_URL', default=None)
AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', default='ap-south-1')

if all([AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, AWS_S3_ENDPOINT_URL]):
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_S3_SIGNATURE_VERSION = 's3v4'
    AWS_S3_ADDRESSING_STYLE = 'path'
    
    # Supabase Professional Optimization:
    # We use Public URLs (no signature) for the media bucket as it's more reliable for IQ tests.
    AWS_QUERYSTRING_AUTH = config('AWS_QUERYSTRING_AUTH', default=False, cast=bool)
    
    # Construct the Custom Domain for Supabase Public Storage
    if '.supabase.co' in AWS_S3_ENDPOINT_URL:
        host = AWS_S3_ENDPOINT_URL.split('//')[1].split('/')[0]
        project_id = host.split('.')[0]
        AWS_S3_CUSTOM_DOMAIN = f"{project_id}.supabase.co/storage/v1/object/public/{AWS_STORAGE_BUCKET_NAME}"
    else:
        AWS_S3_CUSTOM_DOMAIN = config('AWS_S3_CUSTOM_DOMAIN', default=None)
    
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None 
else:
    # Diagnostic Logging to find the missing variable
    import sys
    missing_vars = []
    if not AWS_ACCESS_KEY_ID: missing_vars.append('AWS_ACCESS_KEY_ID')
    if not AWS_SECRET_ACCESS_KEY: missing_vars.append('AWS_SECRET_ACCESS_KEY')
    if not AWS_STORAGE_BUCKET_NAME: missing_vars.append('AWS_STORAGE_BUCKET_NAME')
    if not AWS_S3_ENDPOINT_URL: missing_vars.append('AWS_S3_ENDPOINT_URL')
    
    logger.error(f"CRITICAL: Missing S3 Credentials! Falling back to BROKEN local storage. Missing: {', '.join(missing_vars)}")
    # We intentionally DO NOT fallback to FileSystemStorage for now to see the error in logs, 
    # but for stability, we essentially default to it but with a loud error.
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# Email backend (configure with actual email service)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@example.com')

# Logging for production (Render uses console only - ephemeral filesystem)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}
