"""Logica de negocio de 'Mi biblioteca': listas personales y progreso de lectura."""

from app.models import ESTADOS_LECTURA, Lectura
from app.repositories import lectura_repository, libro_repository
from app.utils import validacion as v
from app.utils.errores import ApiError


def listar(usuario_id, estado=None, favorito=None):
    if estado and estado not in ESTADOS_LECTURA:
        raise ApiError(f"Estado no válido. Use: {', '.join(ESTADOS_LECTURA)}", 400)
    fav = None
    if favorito is not None:
        if favorito not in ("true", "false"):
            raise ApiError("El parametro 'favorito' debe ser true o false", 400)
        fav = favorito == "true"
    return [l.to_dict() for l in lectura_repository.listar(usuario_id, estado, fav)]


def obtener(usuario_id, libro_id):
    lectura = lectura_repository.buscar(usuario_id, libro_id)
    return lectura.to_dict() if lectura else None


def guardar(usuario_id, libro_id, datos):
    """Crea o actualiza (upsert) la lectura del usuario para un libro."""
    if not libro_repository.obtener(libro_id):
        raise ApiError("El libro no existe", 404)

    errores = {}
    estado = datos.get("estado")
    if estado is not None and estado not in ESTADOS_LECTURA:
        errores["estado"] = f"Debe ser uno de: {', '.join(ESTADOS_LECTURA)}"
    favorito = datos.get("favorito")
    if favorito is not None and not isinstance(favorito, bool):
        errores["favorito"] = "Debe ser true o false"
    pagina = v.entero(datos, "pagina_actual", errores, requerido=False, minimo=0)
    total = v.entero(datos, "total_paginas", errores, requerido=False, minimo=1)
    v.lanzar_si_hay_errores(errores)

    lectura = lectura_repository.buscar(usuario_id, libro_id) or Lectura(
        usuario_id=usuario_id, libro_id=libro_id
    )
    if total is not None:
        lectura.total_paginas = total
    if pagina is not None:
        lectura.pagina_actual = min(pagina, lectura.total_paginas or pagina)
        # Reglas de negocio: avanzar marca 'leyendo'; llegar al final marca 'leido'.
        if estado is None and lectura.total_paginas:
            if lectura.pagina_actual >= lectura.total_paginas:
                lectura.estado = "leido"
            elif lectura.pagina_actual > 0 and lectura.estado != "leido":
                lectura.estado = "leyendo"
    if estado is not None:
        lectura.estado = estado
    if favorito is not None:
        lectura.favorito = favorito

    return lectura_repository.guardar(lectura).to_dict()


def eliminar(usuario_id, libro_id):
    lectura = lectura_repository.buscar(usuario_id, libro_id)
    if not lectura:
        raise ApiError("Ese libro no está en tu biblioteca", 404)
    lectura_repository.eliminar(lectura)
