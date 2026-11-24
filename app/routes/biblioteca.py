from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.services import lectura_service
from app.utils.seguridad import usuario_actual_id
from app.utils.validacion import leer_json

biblioteca_bp = Blueprint("biblioteca", __name__, url_prefix="/api/mi-biblioteca")


@biblioteca_bp.get("")
@jwt_required()
def listar():
    """GET /api/mi-biblioteca?estado=leyendo&favorito=true"""
    return jsonify(
        lectura_service.listar(
            usuario_actual_id(), request.args.get("estado"), request.args.get("favorito")
        )
    )


@biblioteca_bp.get("/<int:libro_id>")
@jwt_required()
def obtener(libro_id):
    return jsonify(lectura_service.obtener(usuario_actual_id(), libro_id))


@biblioteca_bp.put("/<int:libro_id>")
@jwt_required()
def guardar(libro_id):
    """Agrega el libro a la biblioteca o actualiza estado, favorito y progreso."""
    return jsonify(lectura_service.guardar(usuario_actual_id(), libro_id, leer_json()))


@biblioteca_bp.delete("/<int:libro_id>")
@jwt_required()
def eliminar(libro_id):
    lectura_service.eliminar(usuario_actual_id(), libro_id)
    return "", 204
