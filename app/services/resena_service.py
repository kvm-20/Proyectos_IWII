"""Logica de negocio de resenas y calificaciones."""

from app.models import Resena
from app.repositories import libro_repository, resena_repository
from app.utils import validacion as v
from app.utils.errores import ApiError


def _libro_o_404(libro_id):
    libro = libro_repository.obtener(libro_id)
    if not libro:
        raise ApiError("El libro no existe", 404)
    return libro


def listar(libro_id, minimo, orden, page, limit):
    _libro_o_404(libro_id)
    if orden not in ("recientes", "calificacion"):
        raise ApiError("El orden debe ser 'recientes' o 'calificacion'", 400)
    items, total = resena_repository.listar_por_libro(libro_id, minimo, orden, page, limit)
    return [r.to_dict() for r in items], total


def crear(libro_id, usuario_id, datos):
    _libro_o_404(libro_id)
    errores = {}
    calificacion = v.entero(datos, "calificacion", errores, minimo=1, maximo=5)
    comentario = v.texto(datos, "comentario", errores, requerido=False, maximo=1000) or ""
    v.lanzar_si_hay_errores(errores)

    if resena_repository.buscar(libro_id, usuario_id):
        raise ApiError("Ya publicaste una reseña para este libro", 409)

    resena = Resena(
        libro_id=libro_id, usuario_id=usuario_id, calificacion=calificacion, comentario=comentario
    )
    return resena_repository.guardar(resena).to_dict()


def eliminar(resena_id, usuario_id, es_admin):
    resena = resena_repository.obtener(resena_id)
    if not resena:
        raise ApiError("La reseña no existe", 404)
    if resena.usuario_id != usuario_id and not es_admin:
        raise ApiError("Solo puedes eliminar tus propias reseñas", 403)
    resena_repository.eliminar(resena)
