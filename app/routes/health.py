from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)


@health_bp.get("/health")
def health():
    """Verifica que el servicio este activo."""
    return jsonify({
        "status": "ok",
        "service": "biblioweb-backend",
        "version": "0.1.0"
    })