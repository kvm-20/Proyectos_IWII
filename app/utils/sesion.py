"""Ayudas para trabajar con el usuario autenticado mediante JWT."""

from functools import wraps

from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from app.repositories import usuario_repository
from app.utils.errors import ErrorAPI


def usuario_actual():
    """Devuelve el usuario dueno del token enviado en la peticion."""
    identidad = get_jwt_identity()
    usuario = usuario_repository.buscar_por_id(int(identidad))
    if usuario is None:
        raise ErrorAPI("La sesion ya no es valida", 401)
    return usuario


def solo_admin(funcion):
    """Restringe un endpoint al rol administrador."""

    @wraps(funcion)
    def envoltura(*args, **kwargs):
        verify_jwt_in_request()
        usuario = usuario_actual()
        if not usuario.es_admin():
            raise ErrorAPI("Solo un administrador puede realizar esta accion", 403)
        return funcion(*args, **kwargs)

    return envoltura
