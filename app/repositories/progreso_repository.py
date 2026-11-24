"""Consultas sobre la tabla de progresos de lectura."""

from app.extensions import db
from app.models import Progreso


def listar_por_usuario(usuario_id, estado=None):
    consulta = Progreso.query.filter_by(usuario_id=usuario_id)
    if estado:
        consulta = consulta.filter_by(estado=estado)
    return consulta.order_by(Progreso.actualizado_en.desc()).all()


def buscar(libro_id, usuario_id):
    return Progreso.query.filter_by(libro_id=libro_id, usuario_id=usuario_id).first()


def guardar(progreso):
    db.session.add(progreso)
    db.session.commit()
    return progreso
