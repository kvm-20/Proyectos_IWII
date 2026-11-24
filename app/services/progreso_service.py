"""Reglas de negocio del progreso de lectura."""

from app.models import Progreso
from app.models.progreso import ESTADOS_VALIDOS
from app.repositories import libro_repository, progreso_repository
from app.utils.errors import ErrorAPI
from app.utils.validators import limpiar_texto, validar_entero


def listar_mis_libros(usuario, estado=None):
    estado = limpiar_texto(estado) or None
    if estado and estado not in ESTADOS_VALIDOS:
        raise ErrorAPI(f"Estado invalido. Valores validos: {', '.join(ESTADOS_VALIDOS)}")
    registros = progreso_repository.listar_por_usuario(usuario.id, estado=estado)
    return [registro.to_dict() for registro in registros]


def actualizar(libro_id, usuario, datos):
    """Guarda la pagina actual y el estado de lectura del usuario."""
    libro = libro_repository.buscar_por_id(libro_id)
    if libro is None:
        raise ErrorAPI("El libro solicitado no existe", 404)

    pagina = validar_entero(datos.get("pagina_actual", 0), "pagina_actual")
    if libro.paginas and pagina > libro.paginas:
        raise ErrorAPI(f"El libro solo tiene {libro.paginas} paginas")

    estado = limpiar_texto(datos.get("estado")) or "leyendo"
    if estado not in ESTADOS_VALIDOS:
        raise ErrorAPI(f"Estado invalido. Valores validos: {', '.join(ESTADOS_VALIDOS)}")

    progreso = progreso_repository.buscar(libro_id, usuario.id)
    if progreso is None:
        progreso = Progreso(libro_id=libro_id, usuario_id=usuario.id)

    progreso.pagina_actual = pagina
    progreso.estado = estado
    progreso_repository.guardar(progreso)
    return progreso.to_dict()
