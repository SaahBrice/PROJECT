"""
Django base settings for FDTM Platform.
Shared settings across all environments.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load environment variables from .env file
load_dotenv(BASE_DIR / '.env')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-change-me-in-production')

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    
    # Third-party apps (will be added as we install them)
    
    # Local apps
    "apps.core",
    "apps.projects",
    "apps.articles",
    "apps.donations",
    "apps.accounts",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",  # For i18n
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "apps.core.middleware.SecurityHeadersMiddleware",
]

# Site URL for payment callbacks
SITE_URL = os.environ.get('SITE_URL', 'http://127.0.0.1:8000')

ROOT_URLCONF = "fdtm.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
                "apps.core.context_processors.site_settings",
                "apps.core.context_processors.language_context",
            ],
        },
    },
]

WSGI_APPLICATION = "fdtm.wsgi.application"

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# =============================================================================
# INTERNATIONALIZATION - French-first, with EN, IT, DE support
# =============================================================================
LANGUAGE_CODE = "fr"  # French as primary language

TIME_ZONE = "Africa/Douala"  # Cameroon timezone

USE_I18N = True
USE_L10N = True
USE_TZ = True

# Supported languages
LANGUAGES = [
    ('fr', 'Français'),
    ('en', 'English'),
    ('it', 'Italiano'),
    ('de', 'Deutsch'),
]

# Path to translation files
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# =============================================================================
# STATIC & MEDIA FILES
# =============================================================================
STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# =============================================================================
# PAYMENT SETTINGS
# =============================================================================
# Stripe
STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY', '')
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY', '')
STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET', '')

# Fapshi
FAPSHI_API_KEY = os.environ.get('FAPSHI_API_KEY', '')
FAPSHI_API_SECRET = os.environ.get('FAPSHI_API_SECRET', '')
FAPSHI_WEBHOOK_SECRET = os.environ.get('FAPSHI_WEBHOOK_SECRET', '')

# =============================================================================
# BACKBLAZE B2 STORAGE SETTINGS
# =============================================================================
B2_APPLICATION_KEY_ID = os.environ.get('B2_APPLICATION_KEY_ID', '')
B2_APPLICATION_KEY = os.environ.get('B2_APPLICATION_KEY', '')
B2_BUCKET_NAME = os.environ.get('B2_BUCKET_NAME', '')
B2_BUCKET_URL = os.environ.get('B2_BUCKET_URL', '')

# =============================================================================
# TRANSLATION API
# =============================================================================
DEEPL_API_KEY = os.environ.get('DEEPL_API_KEY', '')

# =============================================================================
# EMAIL SETTINGS
# =============================================================================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@fdtm.org')
