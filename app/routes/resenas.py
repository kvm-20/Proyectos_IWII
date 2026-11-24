"""Rutas de resenas y calificaciones."""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.services import resena_service
from app.utils.sesion import usuario_actual

resenas_bp = Blueprint("resenas", __name__)


@resenas_bp.get("/api/libros/<int:libro_id>/resenas")
def listar(libro_id):
    """Lista las resenas publicadas sobre un libro."""
    resenas = resena_service.listar_por_libro(libro_id)
    return jsonify({"total": len(resenas), "resenas": resenas}), 200


@resenas_bp.post("/api/libros/<int:libro_id>/resenas")
@jwt_required()
def publicar(libro_id):
    """Crea o actualiza la resena del usuario autenticado."""
    resena = resena_service.crear_o_actualizar(
        libro_id, usuario_actual(), request.get_json(silent=True) or {}
    )
    return jsonify(resena), 201


@resenas_bp.delete("/api/libros/<int:libro_id>/resenas")
@jwt_required()
def eliminar(libro_id):
    """Elimina la resena del usuario autenticado sobre ese libro."""
    resena_service.eliminar(libro_id, usuario_actual())
    return jsonify({"mensaje": "Resena eliminada"}), 200
