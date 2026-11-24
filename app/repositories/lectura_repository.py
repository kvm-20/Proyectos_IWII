"""Acceso a datos de la biblioteca personal (lecturas y progreso)."""

from sqlalchemy import select

from app.extensions import db
from app.models import Lectura


def listar(usuario_id, estado=None, favorito=None):
    consulta = select(Lectura).where(Lectura.usuario_id == usuario_id)
    if estado:
        consulta = consulta.where(Lectura.estado == estado)
    if favorito is not None:
        consulta = consulta.where(Lectura.favorito == favorito)
    consulta = consulta.order_by(Lectura.actualizado_en.desc(), Lectura.id.desc())
    return db.session.scalars(consulta).all()


def buscar(usuario_id, libro_id):
    return db.session.scalar(
        select(Lectura).where(Lectura.usuario_id == usuario_id, Lectura.libro_id == libro_id)
    )


def guardar(lectura):
    db.session.add(lectura)
    db.session.commit()
    return lectura


def eliminar(lectura):
    db.session.delete(lectura)
    db.session.commit()
