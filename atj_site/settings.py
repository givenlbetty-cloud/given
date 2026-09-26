import dj_database_url
from pathlib import Path
import os
from dotenv import load_dotenv, dotenv_values
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")
load_dotenv(BASE_DIR / ".env.production")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-change-me-in-production")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "True").strip().lower() in {"1", "true", "yes", "on"}
if os.environ.get("VERCEL_ENV") == "production":
    # Never expose Django's debug traceback to public production requests.
    DEBUG = False

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")

CSRF_TRUSTED_ORIGINS = [
    'https://localhost:8000',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'https://atj-beta.onrender.com',
    'https://*.app.github.dev',
    'https://*.github.dev',
    'https://*.onrender.com',
]
if 'RENDER_EXTERNAL_HOSTNAME' in os.environ:
    CSRF_TRUSTED_ORIGINS.append(f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}")

INSTALLED_APPS = [
    'chat',
    'jazzmin',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    
    # Third-party
    "crispy_forms",
    "crispy_bootstrap5",

    # Allauth (Google OAuth)
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",

    # Local Apps
    "core",
    "accounts",
    "formations",
    "mentoring",
    "blog",
    "library",
    "storages",
]

MIDDLEWARE = [
    "core.middleware.EnsureSiteMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
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
                "core.context_processors.site_settings",
            ],
        },
    },
]

WSGI_APPLICATION = "atj_site.wsgi.application"

db_url = (
    os.environ.get("SUPABASE_POSTGRES_URL")
    or os.environ.get("SUPABASE_POSTGRES_URL_NON_POOLING")
    or os.environ.get("DATABASE_URL")
)

if not db_url:
    raise RuntimeError(
        "No database URL is configured. Set DATABASE_URL or SUPABASE_POSTGRES_URL."
    )

# Supabase URLs may include the provider-specific `supa` flag, which libpq
# does not recognize as a PostgreSQL connection option.
db_url_parts = urlsplit(db_url)
if db_url_parts.scheme.lower() in {"postgres", "postgresql"}:
    db_query = [
        (key, value)
        for key, value in parse_qsl(db_url_parts.query, keep_blank_values=True)
        if key.lower() != "supa"
    ]
    db_url = urlunsplit(db_url_parts._replace(query=urlencode(db_query)))

DATABASES = {
    "default": dj_database_url.parse(
        db_url,
        conn_max_age=600,
        ssl_require=db_url.startswith(("postgres://", "postgresql://")),
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# WhiteNoise : CompressedStaticFilesStorage (sans Manifest pour éviter les erreurs 404 CSS/JS)
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

# Email Configuration (Console Backend for Development)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Auth
AUTH_USER_MODEL = "accounts.CustomUser"
LOGIN_REDIRECT_URL = "accounts:dashboard"
LOGOUT_REDIRECT_URL = "home"

# Crispy
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Security
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
X_FRAME_OPTIONS = 'SAMEORIGIN'

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Jazzmin Settings
JAZZMIN_SETTINGS = {
    "site_title": "ATJ Admin",
    "site_header": "ATJ Administration",
    "site_brand": "ATJ",
    "site_logo": "img/logo.jpeg",
    "login_logo": "img/logo.jpeg",
    "welcome_sign": "⚠️ Bienvenue dans l'administration ATJ",
    "copyright": "Académie Tremplin de la Jeunesse - Lubumbashi",
    "search_model": "accounts.CustomUser",
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": [
        "accounts",
        "formations",
        "mentoring",
        "blog",
        "library",
        "chat",
        "core",
        "auth",
        "sites",
        "socialaccount",
        "account",
    ],
    "custom_links": {},
    "icons": {
        "accounts.CustomUser": "fas fa-users",
        "auth.Group": "fas fa-users-cog",
        "sites.Site": "fas fa-globe",
        "socialaccount.SocialApp": "fab fa-google",
        "socialaccount.SocialAccount": "fas fa-user-circle",
        "socialaccount.SocialToken": "fas fa-key",
        "account.EmailAddress": "fas fa-envelope",
        "formations.Programme": "fas fa-graduation-cap",
        "formations.Session": "fas fa-calendar-alt",
        "formations.Chapitre": "fas fa-book",
        "formations.Lecon": "fas fa-play-circle",
        "formations.Inscription": "fas fa-clipboard-list",
        "formations.Paiement": "fas fa-credit-card",
        "mentoring.Mentor": "fas fa-chalkboard-teacher",
        "blog.Article": "fas fa-newspaper",
        "blog.Ressource": "fas fa-folder-open",
        "blog.Event": "fas fa-calendar-check",
        "library.Livre": "fas fa-book-open",
        "library.AchatLivre": "fas fa-shopping-cart",
        "library.Note": "fas fa-sticky-note",
        "library.Avis": "fas fa-star",
        "library.Favori": "fas fa-heart",
        "chat.Thread": "fas fa-comments",
        "chat.Message": "fas fa-comment",
        "core.SiteSettings": "fas fa-cogs",
        "core.TeamMember": "fas fa-user-tie",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": True,
    "custom_css": "css/jazzmin-custom.css",

    "use_google_fonts_cdn": True,
    "show_ui_builder": True,
    "topmenu_links": [
        {"name": "Accueil", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Site Public", "url": "home", "new_window": True},
        {"name": "Support", "url": "https://wa.me/24385433976", "new_window": True, "icon": "fab fa-whatsapp"},
    ],
    "usermenu_links": [
        {"name": "Mon Profil", "url": "accounts:profile", "new_window": False, "icon": "fas fa-user"},
    ],
    "language_chooser": False,
}

JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
    "dark_mode_theme": "darkly",
    "navbar": "navbar-dark",
    "navbar_small_text": False,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_flat_style": False,
    "body_small_text": False,
    "brand_small_text": True,
    "accent": "accent-primary",
    "navbar_fixed": True,
    "layout_boxed": False,
}

# ==============================
# DJANGO ALLAUTH + GOOGLE OAUTH
# ==============================
SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# Allauth settings
ACCOUNT_LOGIN_METHODS = {"username", "email"}
ACCOUNT_EMAIL_VERIFICATION = "optional"
ACCOUNT_SIGNUP_FIELDS = ["email*", "username*"]
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {"access_type": "online"},
    }
}

LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "accounts:dashboard"

# Configuration du stockage d'images sur Supabase (S3)
AWS_ACCESS_KEY_ID = os.environ.get('SUPABASE_S3_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('SUPABASE_S3_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'images' # Le nom du bucket que vous avez créé
AWS_S3_ENDPOINT_URL = os.environ.get('SUPABASE_S3_ENDPOINT_URL')
AWS_S3_REGION_NAME = 'us-east-1' # Ou la région indiquée dans Supabase

# Ne pas rajouter de signatures complexes dans l'URL des images
AWS_QUERYSTRING_AUTH = False

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# Dire à Django d'utiliser ce stockage pour les fichiers médias
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}
