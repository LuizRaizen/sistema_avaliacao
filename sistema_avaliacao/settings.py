"""
Configurações Django para o projeto sistema_avaliacao.

Preparado para dev e produção (ex.: Render) usando variáveis de ambiente.
"""

from pathlib import Path
from decouple import config
import os
import dj_database_url

# =========================
# BASE
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# SEGURANÇA
# =========================
SECRET_KEY = config("SECRET_KEY", default="dev-insecure-key")
DEBUG = config("DEBUG", default=False, cast=bool)

# Hosts/CSRF (Render + local)
RENDER_HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")  # ex.: sistema-avaliacao-xxx.onrender.com

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    ".onrender.com",  # wildcard para qualquer subdomínio no Render
]
if RENDER_HOSTNAME and RENDER_HOSTNAME not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(RENDER_HOSTNAME)

# CSRF: confie no domínio do Render e no seu domínio próprio se houver
CSRF_TRUSTED_ORIGINS = [
    "https://*.onrender.com",
]
if RENDER_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(f"https://{RENDER_HOSTNAME}")

# Em produção atrás de proxy (Render usa TLS na borda)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True

# Endurecer cookies/segurança quando não estiver em DEBUG
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    # HSTS (opcional; ajuste a duração depois que tudo estiver ok em HTTPS)
    SECURE_HSTS_SECONDS = 60 * 60 * 24  # 1 dia (aumente para 31536000 após validar)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True

# =========================
# APPS
# =========================
INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Apps do projeto
    "core",
]

# =========================
# MIDDLEWARE
# =========================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # WhiteNoise logo após SecurityMiddleware

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# =========================
# URLS / WSGI
# =========================
ROOT_URLCONF = "sistema_avaliacao.urls"
WSGI_APPLICATION = "sistema_avaliacao.wsgi.application"

# =========================
# TEMPLATES
# =========================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # coloque seus templates globais em BASE_DIR / "templates"
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# =========================
# BANCO DE DADOS
# =========================
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            ssl_require=True,  # Render Postgres com SSL
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# =========================
# VALIDAÇÃO DE SENHAS
# =========================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# =========================
# INTERNACIONALIZAÇÃO
# =========================
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# =========================
# ARQUIVOS ESTÁTICOS & MÍDIA
# =========================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
# se você tem uma pasta local "static/" para assets do projeto:
STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# WhiteNoise - otimização e manifest de estáticos (requer collectstatic ok)
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

# =========================
# LOGIN/LOGOUT
# =========================
LOGIN_URL = "core:login"
LOGIN_REDIRECT_URL = "core:lista_avaliacoes"
LOGOUT_REDIRECT_URL = "core:lista_avaliacoes"

# =========================
# LOGGING (para ver stack traces no Render)
# =========================
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {
        # Exceções de views/middlewares
        "django.request": {"handlers": ["console"], "level": "ERROR", "propagate": False},
        "django.server": {"handlers": ["console"], "level": "ERROR", "propagate": False},
    },
}

# =========================
# OUTRAS CONFIGURAÇÕES
# =========================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
