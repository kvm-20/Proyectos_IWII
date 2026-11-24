"""Rutas del progreso de lectura y de las listas personales."""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.services import progreso_service
from app.utils.sesion import usuario_actual

progreso_bp = Blueprint("progreso", __name__)


@progreso_bp.get("/api/progreso")
@jwt_required()
def mis_libros():
    """Lista los libros del usuario. Acepta el filtro ?estado=."""
    registros = progreso_service.listar_mis_libros(
        usuario_actual(), estado=request.args.get("estado")
    )
    return jsonify({"total": len(registros), "progresos": registros}), 200


@progreso_bp.put("/api/libros/<int:libro_id>/progreso")
@jwt_required()
def actualizar(libro_id):
    """Guarda la pagina actual y el estado de lectura del usuario."""
    progreso = progreso_service.actualizar(
        libro_id, usuario_actual(), request.get_json(silent=True) or {}
    )
    return jsonify(progreso), 200
