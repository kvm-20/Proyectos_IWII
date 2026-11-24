"""Carga datos de ejemplo en la base de datos de BiblioWeb.

Uso:  python seed.py
"""

from app import create_app
from app.extensions import db
from app.models import Libro, Usuario

USUARIOS = [
    {
        "nombre": "Administrador BiblioWeb",
        "correo": "admin@biblioweb.com",
        "contrasena": "admin2026",
        "rol": "admin",
    },
    {
        "nombre": "Karen Vargas",
        "correo": "karen@biblioweb.com",
        "contrasena": "lector2026",
        "rol": "lector",
    },
]

LIBROS = [
    {
        "titulo": "Cien anos de soledad",
        "autor": "Gabriel Garcia Marquez",
        "categoria": "Novela",
        "anio": 1967,
        "paginas": 471,
        "formato": "EPUB",
        "descripcion": "La historia de la familia Buendia en el pueblo de Macondo.",
    },
    {
        "titulo": "La voragine",
        "autor": "Jose Eustasio Rivera",
        "categoria": "Novela",
        "anio": 1924,
        "paginas": 322,
        "formato": "PDF",
        "descripcion": "Relato de la explotacion cauchera en la selva colombiana.",
    },
    {
        "titulo": "Maria",
        "autor": "Jorge Isaacs",
        "categoria": "Novela",
        "anio": 1867,
        "paginas": 304,
        "formato": "EPUB",
        "descripcion": "Novela romantica ambientada en el Valle del Cauca.",
    },
    {
        "titulo": "Ingenieria de software",
        "autor": "Ian Sommerville",
        "categoria": "Tecnologia",
        "anio": 2011,
        "paginas": 792,
        "formato": "PDF",
        "descripcion": "Texto de referencia sobre procesos y practicas de software.",
    },
    {
        "titulo": "Clean Code",
        "autor": "Robert C. Martin",
        "categoria": "Tecnologia",
        "anio": 2008,
        "paginas": 464,
        "formato": "PDF",
        "descripcion": "Principios y practicas para escribir codigo legible.",
    },
    {
        "titulo": "El principito",
        "autor": "Antoine de Saint-Exupery",
        "categoria": "Infantil",
        "anio": 1943,
        "paginas": 96,
        "formato": "EPUB",
        "descripcion": "Relato sobre la amistad y la mirada de la infancia.",
    },
    {
        "titulo": "Breve historia del tiempo",
        "autor": "Stephen Hawking",
        "categoria": "Divulgacion",
        "anio": 1988,
        "paginas": 256,
        "formato": "PDF",
        "descripcion": "Introduccion a la cosmologia para publico general.",
    },
    {
        "titulo": "El laberinto de la soledad",
        "autor": "Octavio Paz",
        "categoria": "Ensayo",
        "anio": 1950,
        "paginas": 191,
        "formato": "EPUB",
        "descripcion": "Ensayo sobre la identidad y la cultura latinoamericana.",
    },
]


def sembrar():
    app = create_app()
    with app.app_context():
        creados_usuarios = 0
        for datos in USUARIOS:
            if Usuario.query.filter_by(correo=datos["correo"]).first():
                continue
            usuario = Usuario(
                nombre=datos["nombre"], correo=datos["correo"], rol=datos["rol"]
            )
            usuario.definir_contrasena(datos["contrasena"])
            db.session.add(usuario)
            creados_usuarios += 1

        creados_libros = 0
        for datos in LIBROS:
            if Libro.query.filter_by(titulo=datos["titulo"]).first():
                continue
            db.session.add(Libro(**datos))
            creados_libros += 1

        db.session.commit()

        print(f"Usuarios creados: {creados_usuarios}")
        print(f"Libros creados:   {creados_libros}")
        print("Base de datos lista.")


if __name__ == "__main__":
    sembrar()
