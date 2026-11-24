"""Logica de negocio del catalogo de libros."""

from datetime import date

from app.models import Libro
from app.repositories import libro_repository
from app.utils import validacion as v
from app.utils.errores import ApiError

CAMPOS_ORDEN = {"titulo", "autor", "anio", "recientes", "calificacion"}


def _a_dict(fila, incluir_contenido=False):
    libro, promedio, total = fila
    return libro.to_dict(promedio=promedio, total_resenas=total, incluir_contenido=incluir_contenido)


def listar(filtros, page, limit):
    orden = filtros.get("orden") or "titulo"
    direccion = filtros.get("direccion") or "asc"
    if orden not in CAMPOS_ORDEN:
        raise ApiError(f"Orden no válido. Use: {', '.join(sorted(CAMPOS_ORDEN))}", 400)
    if direccion not in ("asc", "desc"):
        raise ApiError("La dirección debe ser 'asc' o 'desc'", 400)

    filas, total = libro_repository.listar(
        q=(filtros.get("q") or "").strip() or None,
        categoria=filtros.get("categoria") or None,
        autor=filtros.get("autor") or None,
        orden=orden,
        direccion=direccion,
        page=page,
        limit=limit,
    )
    return [_a_dict(f) for f in filas], total


def obtener(libro_id, incluir_contenido=False):
    fila = libro_repository.obtener_con_calificacion(libro_id)
    if not fila:
        raise ApiError("El libro no existe", 404)
    return _a_dict(fila, incluir_contenido)


def _validar(datos, parcial=False):
    errores = {}
    requerido = not parcial
    limpio = {}
    if not parcial or "titulo" in datos:
        limpio["titulo"] = v.texto(datos, "titulo", errores, requerido, maximo=200)
    if not parcial or "autor" in datos:
        limpio["autor"] = v.texto(datos, "autor", errores, requerido, minimo=2, maximo=150)
    if not parcial or "categoria" in datos:
        limpio["categoria"] = v.texto(datos, "categoria", errores, requerido, minimo=3, maximo=60)
    if "anio" in datos:
        limpio["anio"] = v.entero(datos, "anio", errores, False, minimo=-3000, maximo=date.today().year)
    if "idioma" in datos:
        limpio["idioma"] = v.texto(datos, "idioma", errores, False, maximo=30)
    if "descripcion" in datos:
        limpio["descripcion"] = v.texto(datos, "descripcion", errores, False, maximo=2000) or ""
    if "contenido" in datos:
        limpio["contenido"] = v.texto(datos, "contenido", errores, False, maximo=200000) or ""
    if "url_externa" in datos:
        url = v.texto(datos, "url_externa", errores, False, maximo=500)
        if url and not url.startswith(("http://", "https://")):
            errores["url_externa"] = "Debe ser una URL que empiece por http:// o https://"
        limpio["url_externa"] = url
    v.lanzar_si_hay_errores(errores)
    return limpio


def crear(datos):
    limpio = _validar(datos)
    if libro_repository.existe(limpio["titulo"], limpio["autor"]):
        raise ApiError("Ya existe un libro con ese título y autor", 409)
    libro = libro_repository.guardar(Libro(**limpio))
    return obtener(libro.id)


def actualizar(libro_id, datos):
    libro = libro_repository.obtener(libro_id)
    if not libro:
        raise ApiError("El libro no existe", 404)
    limpio = _validar(datos, parcial=True)
    titulo = limpio.get("titulo") or libro.titulo
    autor = limpio.get("autor") or libro.autor
    if libro_repository.existe(titulo, autor, excluir_id=libro.id):
        raise ApiError("Ya existe un libro con ese título y autor", 409)
    for campo, valor in limpio.items():
        setattr(libro, campo, valor)
    libro_repository.guardar(libro)
    return obtener(libro.id)


def eliminar(libro_id):
    libro = libro_repository.obtener(libro_id)
    if not libro:
        raise ApiError("El libro no existe", 404)
    libro_repository.eliminar(libro)


def categorias():
    return libro_repository.categorias()
