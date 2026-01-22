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

# DATABASE CONFIGURATION (Supabase High-Latency Stability Fix)
# Using Port 6543 (Transaction Mode) - Lightweight and scalable.
# We explicitly DISABLE server-side cursors for compatibility.
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL'),
        conn_max_age=0, # Disable pooling to prevent 'stale' transaction errors
    )
}

# Essential PostgreSQL Options for Supabase Transaction Pooler
DATABASES['default']['OPTIONS'] = {
    'sslmode': 'require',
    'connect_timeout': 30, 
}

# DISABLE server-side cursors - REQUIRED for Transaction Mode (Port 6543)
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
    AWS_QUERYSTRING_AUTH = config('AWS_QUERYSTRING_AUTH', default=False, cast=bool)
    
    # Construct the Custom Domain for Supabase Public Storage
    if '.supabase.co' in AWS_S3_ENDPOINT_URL:
        # Extract project_id carefully from different formats:
        host = AWS_S3_ENDPOINT_URL.split('//')[1].split('/')[0]
        project_id = host.split('.')[0]
        AWS_S3_CUSTOM_DOMAIN = f"{project_id}.supabase.co/storage/v1/object/public/{AWS_STORAGE_BUCKET_NAME}"
    else:
        AWS_S3_CUSTOM_DOMAIN = config('AWS_S3_CUSTOM_DOMAIN', default=None)
    
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None # Supabase handles ACLs via bucket settings
else:
    # Fallback to local storage if S3 not configured
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
