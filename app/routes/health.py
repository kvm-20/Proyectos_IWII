from flask import Blueprint, jsonify
from sqlalchemy import text

from app.extensions import db

health_bp = Blueprint("health", __name__)


@health_bp.get("/health")
def health():
    """Verifica que el servicio y la base de datos esten activos."""
    try:
        db.session.execute(text("SELECT 1"))
        estado_db = "ok"
    except Exception:
        estado_db = "error"
    return jsonify({
        "status": "ok",
        "service": "biblioweb-backend",
        "version": "1.0.0",
        "database": estado_db,
    })
