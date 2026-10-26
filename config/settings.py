"""
Configurações do projeto site-portfolio.

Tudo o que muda entre o seu computador e o servidor (chave secreta, DEBUG,
domínio) vem do arquivo .env, que NÃO vai pro GitHub. O resto é fixo.
"""

import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

# Pasta raiz do projeto (onde fica o manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent

# Lê o arquivo .env da raiz e coloca as variáveis em os.environ
load_dotenv(BASE_DIR / ".env")


# --- Segurança ---------------------------------------------------------------

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ImproperlyConfigured(
        "SECRET_KEY não definida. Copie o .env.example para .env e preencha."
    )

# Só liga o DEBUG se o .env disser exatamente DEBUG=True
DEBUG = os.getenv("DEBUG", "False") == "True"

# Domínios que podem servir o site, separados por vírgula no .env
# Ex.: ALLOWED_HOSTS=thiagolimeira.pythonanywhere.com
ALLOWED_HOSTS = [h.strip() for h in os.getenv("ALLOWED_HOSTS", "").split(",") if h.strip()]
if DEBUG:
    ALLOWED_HOSTS += ["localhost", "127.0.0.1"]

# O login do admin é um formulário POST. Em HTTPS o Django confere se o
# formulário veio do próprio site; aqui dizemos quais origens são confiáveis.
CSRF_TRUSTED_ORIGINS = [
    f"https://{h}" for h in ALLOWED_HOSTS if h not in ("localhost", "127.0.0.1")
]

if not DEBUG:
    # Em produção os cookies de sessão e CSRF só trafegam por HTTPS
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True


# --- Apps ----------------------------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Apps do portfólio
    "core",
    "projetos",
    "tecnologias",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # Pasta de templates compartilhados (base.html, 404.html)
        "DIRS": [BASE_DIR / "templates"],
        # Cada app também tem a sua pasta templates/
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # Deixa o perfil disponível em todos os templates
                "core.context_processors.perfil",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# --- Banco de dados ------------------------------------------------------------

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# --- Senhas --------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# --- Idioma e fuso -------------------------------------------------------------

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True


# --- Arquivos estáticos (CSS, JS) e de mídia (uploads) -------------------------

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]  # onde você escreve o CSS e o JS
STATIC_ROOT = BASE_DIR / "staticfiles"  # onde o collectstatic junta tudo no servidor

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"  # prints e foto enviados pelo admin
