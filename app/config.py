import os
from datetime import timedelta

from dotenv import load_dotenv

# Carga las variables del archivo .env (si existe) al entorno.
load_dotenv()


def _lista(valor):
    return [v.strip() for v in valor.split(",") if v.strip()]


class Config:
    """Configuracion base de la aplicacion BiblioWeb.

    Todos los valores se pueden sobrescribir con variables de entorno,
    asi las credenciales nunca quedan escritas en el codigo.
    """

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-biblioweb-2026")
    JSON_SORT_KEYS = False
    DEBUG = os.environ.get("FLASK_DEBUG", "true").lower() == "true"

    # Base de datos: MySQL en Docker/Kubernetes, SQLite en desarrollo local.
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///biblioweb.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}

    # JWT
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev-jwt-biblioweb-2026-cambiar-en-produccion")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=int(os.environ.get("JWT_HOURS", "8")))

    # CORS: origenes del frontend autorizados
    CORS_ORIGINS = _lista(
        os.environ.get(
            "CORS_ORIGINS",
            "http://localhost:5173,http://127.0.0.1:5173,http://localhost:8080",
        )
    )

    # Metricas para Prometheus (/metrics)
    METRICS_ENABLED = os.environ.get("METRICS_ENABLED", "true").lower() == "true"

    # Usuarios iniciales (seed)
    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@biblioweb.com")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "Admin123*")


class TestConfig(Config):
    """Configuracion para pruebas automaticas: base de datos en memoria."""

    TESTING = True
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    METRICS_ENABLED = False
    JWT_SECRET_KEY = "clave-de-pruebas-con-longitud-suficiente-32b"
