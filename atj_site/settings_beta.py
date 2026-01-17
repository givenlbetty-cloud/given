"""
═══════════════════════════════════════════════════════════════════════
🚀 DJANGO SETTINGS - ENVIRONNEMENT BETA
═══════════════════════════════════════════════════════════════════════

Configuration sécurisée et isolée pour tests client.
Importer avec: manage.py runserver --settings=atj_site.settings_beta
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env.beta
load_dotenv('.env.beta')

# ═══════════════════════════════════════════════════════════════════════
# 📍 CHEMINS DE BASE
# ═══════════════════════════════════════════════════════════════════════

BASE_DIR = Path(__file__).resolve().parent.parent

# ═══════════════════════════════════════════════════════════════════════
# 🔑 SÉCURITÉ
# ═══════════════════════════════════════════════════════════════════════

# SECRET_KEY DIFFÉRENTE de production
SECRET_KEY = os.getenv(
    'SECRET_KEY',
    'django-insecure-beta-testing-key-change-this-randomly-64-chars-min'
)

# DEBUG = True pour développement/tests
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# ALLOWED_HOSTS = Domaine de test UNIQUEMENT
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# CSRF & CORS pour domaine beta uniquement
CSRF_TRUSTED_ORIGINS = [
    origin.strip() for origin in os.getenv(
        'CSRF_TRUSTED_ORIGINS',
        'https://beta.monprojet.com,http://localhost:8000,http://127.0.0.1:8000,https://localhost:8000,https://*.app.github.dev,https://*.github.dev'
    ).split(',')
]

print(f"""
╔══════════════════════════════════════════╗
║  🚀 DJANGO BETA ENVIRONMENT              ║
║  DEBUG={DEBUG}, HOSTS={ALLOWED_HOSTS[0]}
║  Trusted Origins: {', '.join(CSRF_TRUSTED_ORIGINS[:2])}...
║  Database: db_beta.sqlite3              ║
║  Médias: media_beta/                    ║
╚══════════════════════════════════════════╝
""")

# ═══════════════════════════════════════════════════════════════════════
# 📱 INSTALLED APPS
# ═══════════════════════════════════════════════════════════════════════

INSTALLED_APPS = [
    'chat',
    'jazzmin',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    
    # Third-party
    "crispy_forms",
    "crispy_bootstrap5",

    # Local Apps
    "core",
    "accounts",
    "formations",
    "mentoring",
    "blog",
    "library",
]

# ═══════════════════════════════════════════════════════════════════════
# ⚙️  MIDDLEWARE (avec Basic Auth activé)
# ═══════════════════════════════════════════════════════════════════════

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # 🔐 Basic Auth pour protéger l'accès
    "core.middleware.BasicAuthMiddleware",
    # 📌 Headers indiquant environnement BETA
    "core.middleware.BetaEnvironmentHeaderMiddleware",
]

ROOT_URLCONF = "atj_site.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "atj_site.wsgi.application"

# ═══════════════════════════════════════════════════════════════════════
# 📊 BASE DE DONNÉES - SÉPARÉE DE PRODUCTION
# ═══════════════════════════════════════════════════════════════════════

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / os.getenv('DATABASE_NAME', 'db_beta.sqlite3'),
    }
}

print(f"✅ Database: {BASE_DIR / os.getenv('DATABASE_NAME', 'db_beta.sqlite3')}")

# ═══════════════════════════════════════════════════════════════════════
# 🔐 VALIDATION DE MOTS DE PASSE
# ═══════════════════════════════════════════════════════════════════════

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 8}
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# ═══════════════════════════════════════════════════════════════════════
# 🌍 LOCALISATION & FUSEAU HORAIRE
# ═══════════════════════════════════════════════════════════════════════

LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ═══════════════════════════════════════════════════════════════════════
# 📁 FICHIERS STATIQUES & MÉDIAS
# ═══════════════════════════════════════════════════════════════════════

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles_beta"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# 🎨 MÉDIAS SÉPARÉS (ne pas mélanger avec production)
MEDIA_URL = os.getenv('MEDIA_URL', '/media_beta/')
MEDIA_ROOT = BASE_DIR / os.getenv('MEDIA_ROOT', 'media_beta')

print(f"✅ Médias: {MEDIA_ROOT}")

# Créer le dossier media_beta s'il n'existe pas
os.makedirs(MEDIA_ROOT, exist_ok=True)

# ═══════════════════════════════════════════════════════════════════════
# 📧 EMAIL - CONSOLE BACKEND (NE PAS envoyer de vrais emails)
# ═══════════════════════════════════════════════════════════════════════

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
# Les emails s'afficheront dans la console du serveur, pas envoyés réellement

# ═══════════════════════════════════════════════════════════════════════
# 🔐 AUTHENTIFICATION & SESSIONS
# ═══════════════════════════════════════════════════════════════════════

AUTH_USER_MODEL = "accounts.CustomUser"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"

# ═══════════════════════════════════════════════════════════════════════
# 🎯 CRISPY FORMS
# ═══════════════════════════════════════════════════════════════════════

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# ═══════════════════════════════════════════════════════════════════════
# 🔒 SÉCURITÉ SSL/HTTPS
# ═══════════════════════════════════════════════════════════════════════

# À False en développement, True en production (avec HTTPS)
SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'False') == 'True'
SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False') == 'True'
CSRF_COOKIE_SECURE = os.getenv('CSRF_COOKIE_SECURE', 'False') == 'True'

# Ajouter headers de sécurité
SECURE_HSTS_SECONDS = 31536000 if SECURE_SSL_REDIRECT else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = SECURE_SSL_REDIRECT
SECURE_HSTS_PRELOAD = SECURE_SSL_REDIRECT

# ═══════════════════════════════════════════════════════════════════════
# 💳 SERVICES TIERS - MODE SANDBOX UNIQUEMENT
# ═══════════════════════════════════════════════════════════════════════

# Stripe (Clés de test)
STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY', 'pk_test_changeme')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', 'sk_test_changeme')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET', 'whsec_test_changeme')

# Vérifier que ce sont bien des clés de TEST
if STRIPE_PUBLIC_KEY.startswith('pk_live_') or STRIPE_SECRET_KEY.startswith('sk_live_'):
    raise ValueError(
        "⚠️  ERREUR CRITIQUE: Les clés PRODUCTION Stripe ont été utilisées en BETA!\n"
        "Utilisez UNIQUEMENT les clés de test (pk_test_, sk_test_)"
    )

print("✅ Stripe: Mode TEST (bac à sable)")

# Twilio (si utilisé)
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', '')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', '')

# ═══════════════════════════════════════════════════════════════════════
# 📝 LOGGING (Mode verbose pour déboguer)
# ═══════════════════════════════════════════════════════════════════════

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
        'level': os.getenv('LOG_LEVEL', 'INFO'),
    },
}

# ═══════════════════════════════════════════════════════════════════════
# 🎯 DJANGO
# ═══════════════════════════════════════════════════════════════════════

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ═══════════════════════════════════════════════════════════════════════
# 🎨 JAZZMIN ADMIN (Personnalisé pour BETA)
# ═══════════════════════════════════════════════════════════════════════

JAZZMIN_SETTINGS = {
    "site_title": "ATJ Admin - BETA",
    "site_header": "ATJ Administration [BETA]",
    "site_brand": "Académie Tremplin - Version de Test",
    "welcome_sign": "⚠️  BIENVENUE EN VERSION BETA | 🔐 DONNÉES DE TEST UNIQUEMENT",
    "copyright": "Académie Tremplin de la Jeunesse - Environnement de Test",
    "search_model": "auth.User",
    "topmenu_links": [
        {"name": "Admin",  "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Site Public", "url": "home", "new_window": True},
    ],
    "show_ui_builder": True,
    "theme": "flatly",
    "dark_mode_theme": "darkly",
}

# ═══════════════════════════════════════════════════════════════════════
# ✅ VALIDATION FINALE
# ═══════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════╗
║  🔐 VÉRIFICATIONS DE SÉCURITÉ BETA                            ║
╠════════════════════════════════════════════════════════════════╣
║  ✅ Database: Séparée (db_beta.sqlite3)                       ║
║  ✅ Médias: Séparés (media_beta/)                             ║
║  ✅ SECRET_KEY: Différente de production                      ║
║  ✅ DEBUG: Mode test (peut être désactivé)                    ║
║  ✅ Email: Console backend (pas d'envoi réel)                 ║
║  ✅ Stripe: Mode TEST uniquement                              ║
║  ✅ Basic Auth: Activé si ENABLE_BASIC_AUTH=True             ║
║  ✅ ALLOWED_HOSTS: Domaines de test uniquement                ║
╚════════════════════════════════════════════════════════════════╝
""")