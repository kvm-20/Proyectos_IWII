"""Acceso a datos de libros (capa de repositorio)."""

from sqlalchemy import func, or_, select

from app.extensions import db
from app.models import Libro, Resena

ORDENES = {
    "titulo": Libro.titulo,
    "autor": Libro.autor,
    "anio": Libro.anio,
    "recientes": Libro.creado_en,
}


def _consulta_con_calificacion():
    """SELECT libro, AVG(calificacion), COUNT(resenas) ... LEFT JOIN resenas GROUP BY libro."""
    promedio = func.coalesce(func.avg(Resena.calificacion), 0).label("promedio")
    total = func.count(Resena.id).label("total_resenas")
    consulta = (
        select(Libro, promedio, total)
        .outerjoin(Resena, Resena.libro_id == Libro.id)
        .group_by(Libro.id)
    )
    return consulta, promedio, total


def listar(q=None, categoria=None, autor=None, orden="titulo", direccion="asc", page=1, limit=8):
    """Consulta con filtros (texto, categoria, autor) y ordenamiento, paginada."""
    consulta, promedio, _ = _consulta_con_calificacion()

    if q:
        patron = f"%{q}%"
        consulta = consulta.where(or_(Libro.titulo.ilike(patron), Libro.autor.ilike(patron)))
    if categoria:
        consulta = consulta.where(Libro.categoria == categoria)
    if autor:
        consulta = consulta.where(Libro.autor.ilike(f"%{autor}%"))

    columna = promedio if orden == "calificacion" else ORDENES.get(orden, Libro.titulo)
    columna = columna.desc() if direccion == "desc" else columna.asc()
    consulta = consulta.order_by(columna, Libro.id)

    total = db.session.scalar(select(func.count()).select_from(consulta.subquery()))
    filas = db.session.execute(consulta.limit(limit).offset((page - 1) * limit)).all()
    return filas, total


def obtener_con_calificacion(libro_id):
    consulta, _, _ = _consulta_con_calificacion()
    return db.session.execute(consulta.where(Libro.id == libro_id)).first()


def obtener(libro_id):
    return db.session.get(Libro, libro_id)


def existe(titulo, autor, excluir_id=None):
    consulta = select(Libro.id).where(
        func.lower(Libro.titulo) == titulo.lower(), func.lower(Libro.autor) == autor.lower()
    )
    if excluir_id:
        consulta = consulta.where(Libro.id != excluir_id)
    return db.session.scalar(consulta) is not None


def categorias():
    filas = db.session.execute(select(Libro.categoria).distinct().order_by(Libro.categoria))
    return [fila[0] for fila in filas]


def guardar(libro):
    db.session.add(libro)
    db.session.commit()
    return libro


def eliminar(libro):
    db.session.delete(libro)
    db.session.commit()
