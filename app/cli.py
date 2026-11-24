"""Comandos de consola:
    flask --app run.py init-db   -> crea las tablas y carga datos iniciales
    flask --app run.py seed      -> solo carga datos iniciales
"""

import time

import click
from flask import current_app
from sqlalchemy.exc import IntegrityError, OperationalError

from app.extensions import db
from app.models import Libro, Resena, Usuario
from app.seed_data import LIBROS, RESENAS_DEMO


def _crear_usuario(nombre, email, password, rol):
    usuario = Usuario.query.filter_by(email=email).first()
    if usuario:
        return usuario
    usuario = Usuario(nombre=nombre, email=email, rol=rol)
    usuario.set_password(password)
    db.session.add(usuario)
    db.session.commit()
    return usuario


def cargar_datos_iniciales():
    try:
        _crear_usuario(
            "Administrador", current_app.config["ADMIN_EMAIL"],
            current_app.config["ADMIN_PASSWORD"], "admin",
        )
        lector = _crear_usuario("Lector Demo", "lector@biblioweb.com", "Lector123*", "lector")

        if Libro.query.count() == 0:
            for datos in LIBROS:
                db.session.add(Libro(**datos))
            db.session.commit()

            for titulo, calificacion, comentario in RESENAS_DEMO:
                libro = Libro.query.filter_by(titulo=titulo).first()
                if libro:
                    db.session.add(Resena(libro_id=libro.id, usuario_id=lector.id,
                                          calificacion=calificacion, comentario=comentario))
            db.session.commit()
    except IntegrityError:
        # Otra replica (por ejemplo en Kubernetes) ya cargo los datos.
        db.session.rollback()


def registrar_comandos(app):
    @app.cli.command("init-db")
    @click.option("--intentos", default=20, help="Reintentos mientras la base de datos arranca")
    def init_db(intentos):
        """Crea las tablas (esperando a que MySQL este listo) y carga los datos iniciales."""
        for intento in range(1, intentos + 1):
            try:
                db.create_all()
                cargar_datos_iniciales()
                click.echo("Base de datos lista.")
                return
            except OperationalError as error:
                db.session.rollback()
                click.echo(f"Esperando la base de datos ({intento}/{intentos}): {error.orig}")
                time.sleep(3)
        raise click.ClickException("No fue posible conectarse a la base de datos")

    @app.cli.command("seed")
    def seed():
        """Carga usuarios y libros de ejemplo."""
        cargar_datos_iniciales()
        click.echo("Datos iniciales cargados.")
