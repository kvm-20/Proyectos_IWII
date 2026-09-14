from flask import Flask
from flask_cors import CORS

from app.routes import health_bp


def create_app():
    """Application factory: construye y devuelve la app Flask."""
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    CORS(app, origins=["http://localhost:5173"])

    app.register_blueprint(health_bp)

    return app