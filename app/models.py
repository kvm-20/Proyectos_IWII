"""Modelos ORM (SQLAlchemy) de BiblioWeb.

Relaciones uno-a-muchos:
  - Un Libro tiene muchas Resenas   (la clave foranea libro_id esta en Resena).
  - Un Usuario tiene muchas Resenas (la clave foranea usuario_id esta en Resena).
  - Un Usuario tiene muchas Lecturas (su lista personal y progreso por libro).
"""

from datetime import datetime, timezone

from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db

ESTADOS_LECTURA = ("pendiente", "leyendo", "leido")


def ahora():
    return datetime.now(timezone.utc)


def _fecha(valor):
    """Las fechas se guardan en UTC; se devuelven en ISO 8601 con zona horaria."""
    if not valor:
        return None
    if valor.tzinfo is None:
        valor = valor.replace(tzinfo=timezone.utc)
    return valor.isoformat()


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(20), nullable=False, default="lector")
    creado_en = db.Column(db.DateTime, default=ahora)

    resenas = db.relationship("Resena", back_populates="usuario", cascade="all, delete-orphan")
    lecturas = db.relationship("Lectura", back_populates="usuario", cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "rol": self.rol,
            "creado_en": _fecha(self.creado_en),
        }


class Libro(db.Model):
    __tablename__ = "libros"
    __table_args__ = (db.UniqueConstraint("titulo", "autor", name="uq_libro_titulo_autor"),)

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False, index=True)
    autor = db.Column(db.String(150), nullable=False, index=True)
    categoria = db.Column(db.String(60), nullable=False, index=True)
    anio = db.Column(db.Integer)
    idioma = db.Column(db.String(30), default="Español")
    descripcion = db.Column(db.Text, default="")
    contenido = db.Column(db.Text, default="")
    url_externa = db.Column(db.String(500))
    creado_en = db.Column(db.DateTime, default=ahora)

    resenas = db.relationship(
        "Resena", back_populates="libro", cascade="all, delete-orphan", passive_deletes=True
    )

    def to_dict(self, promedio=None, total_resenas=None, incluir_contenido=False):
        datos = {
            "id": self.id,
            "titulo": self.titulo,
            "autor": self.autor,
            "categoria": self.categoria,
            "anio": self.anio,
            "idioma": self.idioma,
            "descripcion": self.descripcion,
            "url_externa": self.url_externa,
            "calificacion_promedio": round(float(promedio or 0), 1),
            "total_resenas": int(total_resenas or 0),
            "creado_en": _fecha(self.creado_en),
        }
        if incluir_contenido:
            datos["contenido"] = self.contenido or ""
        return datos


class Resena(db.Model):
    __tablename__ = "resenas"
    __table_args__ = (db.UniqueConstraint("libro_id", "usuario_id", name="uq_resena_libro_usuario"),)

    id = db.Column(db.Integer, primary_key=True)
    calificacion = db.Column(db.Integer, nullable=False)
    comentario = db.Column(db.Text, default="")
    libro_id = db.Column(db.Integer, db.ForeignKey("libros.id", ondelete="CASCADE"), nullable=False, index=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    creado_en = db.Column(db.DateTime, default=ahora)

    libro = db.relationship("Libro", back_populates="resenas")
    usuario = db.relationship("Usuario", back_populates="resenas")

    def to_dict(self):
        return {
            "id": self.id,
            "calificacion": self.calificacion,
            "comentario": self.comentario,
            "libro_id": self.libro_id,
            "usuario": {"id": self.usuario.id, "nombre": self.usuario.nombre},
            "creado_en": _fecha(self.creado_en),
        }


class Lectura(db.Model):
    """Lista personal del lector y su progreso en cada libro."""

    __tablename__ = "lecturas"
    __table_args__ = (db.UniqueConstraint("usuario_id", "libro_id", name="uq_lectura_usuario_libro"),)

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    libro_id = db.Column(db.Integer, db.ForeignKey("libros.id", ondelete="CASCADE"), nullable=False, index=True)
    estado = db.Column(db.String(20), nullable=False, default="pendiente")
    favorito = db.Column(db.Boolean, nullable=False, default=False)
    pagina_actual = db.Column(db.Integer, nullable=False, default=0)
    total_paginas = db.Column(db.Integer, nullable=False, default=1)
    actualizado_en = db.Column(db.DateTime, default=ahora, onupdate=ahora)

    usuario = db.relationship("Usuario", back_populates="lecturas")
    libro = db.relationship("Libro")

    @property
    def porcentaje(self):
        if not self.total_paginas:
            return 0
        return min(100, round(self.pagina_actual / self.total_paginas * 100))

    def to_dict(self):
        return {
            "libro": {
                "id": self.libro.id,
                "titulo": self.libro.titulo,
                "autor": self.libro.autor,
                "categoria": self.libro.categoria,
            },
            "estado": self.estado,
            "favorito": self.favorito,
            "pagina_actual": self.pagina_actual,
            "total_paginas": self.total_paginas,
            "porcentaje": self.porcentaje,
            "actualizado_en": _fecha(self.actualizado_en),
        }
