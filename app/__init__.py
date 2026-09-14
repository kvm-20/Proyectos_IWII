from flask import Flask

from app.routes import health_bp


def create_app():
    """Application factory: construye y devuelve la app Flask."""
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    app.register_blueprint(health_bp)

    return app