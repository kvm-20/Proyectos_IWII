from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from app.repositories import usuario_repository
from app.services import auth_service
from app.utils.errores import ApiError
from app.utils.seguridad import usuario_actual_id
from app.utils.validacion import leer_json

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.post("/register")
def register():
    usuario = auth_service.registrar(leer_json())
    return jsonify({"mensaje": "Usuario creado correctamente", "usuario": usuario.to_dict()}), 201


@auth_bp.post("/login")
def login():
    return jsonify(auth_service.iniciar_sesion(leer_json())), 200


@auth_bp.get("/me")
@jwt_required()
def me():
    usuario = usuario_repository.obtener(usuario_actual_id())
    if not usuario:
        raise ApiError("El usuario ya no existe", 404)
    return jsonify(usuario.to_dict())
