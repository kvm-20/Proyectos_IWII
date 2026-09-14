import os


class Config:
    """Configuracion base de la aplicacion BiblioWeb."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-biblioweb-2026")
    JSON_SORT_KEYS = False
    DEBUG = True