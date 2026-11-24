"""Middleware de autenticacion y autorizacion basado en JWT."""

from functools import wraps

from flask_jwt_extended import get_jwt, get_jwt_identity, verify_jwt_in_request

from app.utils.errores import ApiError, respuesta_error


def usuario_actual_id():
    return int(get_jwt_identity())


def es_admin():
    return get_jwt().get("rol") == "admin"


def admin_requerido(funcion):
    """Protege una ruta: exige token valido (401) y rol admin (403)."""

    @wraps(funcion)
    def envoltura(*args, **kwargs):
        verify_jwt_in_request()
        if not es_admin():
            raise ApiError("Solo un administrador puede realizar esta acción", 403)
        return funcion(*args, **kwargs)

    return envoltura


def configurar_jwt(jwt):
    """Respuestas JSON en espanol cuando el token falla."""

    @jwt.unauthorized_loader
    def sin_token(motivo):
        return respuesta_error("Debe iniciar sesión: falta el token de acceso", 401)

    @jwt.invalid_token_loader
    def token_invalido(motivo):
        return respuesta_error("El token de acceso no es válido", 401)

    @jwt.expired_token_loader
    def token_expirado(header, payload):
        return respuesta_error("La sesión expiró, inicie sesión de nuevo", 401)
