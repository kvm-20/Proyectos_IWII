"""Acceso a datos de resenas (lado 'muchos' de Libro -> Resenas)."""

from sqlalchemy import func, select

from app.extensions import db
from app.models import Resena


def listar_por_libro(libro_id, minimo=None, orden="recientes", page=1, limit=10):
    """Consulta filtrada sobre datos relacionados: resenas de un libro,
    con calificacion minima opcional y ordenadas por fecha o calificacion."""
    consulta = select(Resena).where(Resena.libro_id == libro_id)
    if minimo:
        consulta = consulta.where(Resena.calificacion >= minimo)
    if orden == "calificacion":
        consulta = consulta.order_by(Resena.calificacion.desc(), Resena.id.desc())
    else:
        consulta = consulta.order_by(Resena.creado_en.desc(), Resena.id.desc())

    total = db.session.scalar(select(func.count()).select_from(consulta.subquery()))
    items = db.session.scalars(consulta.limit(limit).offset((page - 1) * limit)).all()
    return items, total


def buscar(libro_id, usuario_id):
    return db.session.scalar(
        select(Resena).where(Resena.libro_id == libro_id, Resena.usuario_id == usuario_id)
    )


def obtener(resena_id):
    return db.session.get(Resena, resena_id)


def guardar(resena):
    db.session.add(resena)
    db.session.commit()
    return resena


def eliminar(resena):
    db.session.delete(resena)
    db.session.commit()
