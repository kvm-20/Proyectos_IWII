from flask import Flask
from flask_cors import CORS

from app.cli import registrar_comandos
from app.extensions import db, jwt
from app.routes import auth_bp, biblioteca_bp, health_bp, libros_bp
from app.utils.errores import registrar_manejadores
from app.utils.middleware import registrar_middleware
from app.utils.seguridad import configurar_jwt


def create_app(config_object="app.config.Config"):
    """Application factory: construye y devuelve la app Flask."""
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.json.sort_keys = False  # respeta el orden de los campos en el JSON

    # Extensiones
    CORS(app, origins=app.config["CORS_ORIGINS"])
    db.init_app(app)
    jwt.init_app(app)
    configurar_jwt(jwt)

    # Middleware (logging) y manejo de errores en JSON
    registrar_middleware(app)
    registrar_manejadores(app)

    # Rutas (Blueprints)
    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(libros_bp)
    app.register_blueprint(biblioteca_bp)

    # Comandos: flask --app run.py init-db
    registrar_comandos(app)

    # Metricas para Prometheus en /metrics
    if app.config.get("METRICS_ENABLED"):
        from prometheus_flask_exporter import PrometheusMetrics

        metricas = PrometheusMetrics(app, group_by="url_rule")
        metricas.info("biblioweb_app_info", "Información de BiblioWeb", version="1.0.0")

    return app
