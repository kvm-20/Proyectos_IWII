from app.routes.auth import auth_bp
from app.routes.biblioteca import biblioteca_bp
from app.routes.health import health_bp
from app.routes.libros import libros_bp

__all__ = ["health_bp", "auth_bp", "libros_bp", "biblioteca_bp"]
