"""Acceso a datos de usuarios."""

from sqlalchemy import select

from app.extensions import db
from app.models import Usuario


def buscar_por_email(email):
    return db.session.scalar(select(Usuario).where(Usuario.email == email.lower()))


def obtener(usuario_id):
    return db.session.get(Usuario, usuario_id)


def guardar(usuario):
    db.session.add(usuario)
    db.session.commit()
    return usuario
