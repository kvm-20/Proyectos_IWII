"""Modelo Progreso: avance de lectura de un usuario sobre un libro."""

from datetime import datetime, timezone

from app.extensions import db

ESTADOS_VALIDOS = ("favorito", "leyendo", "leido")


class Progreso(db.Model):
    """Registro del avance de lectura y del estado del libro para un usuario."""

    __tablename__ = "progresos"
    __table_args__ = (
        db.UniqueConstraint("libro_id", "usuario_id", name="uq_progreso_libro_usuario"),
    )

    id = db.Column(db.Integer, primary_key=True)
    libro_id = db.Column(
        db.Integer, db.ForeignKey("libros.id", ondelete="CASCADE"), nullable=False
    )
    usuario_id = db.Column(
        db.Integer, db.ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False
    )
    pagina_actual = db.Column(db.Integer, default=0, nullable=False)
    estado = db.Column(db.String(20), default="leyendo", nullable=False)
    actualizado_en = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    libro = db.relationship("Libro", back_populates="progresos")
    usuario = db.relationship("Usuario", back_populates="progresos")

    def porcentaje(self):
        """Porcentaje leido respecto al total de paginas del libro."""
        if not self.libro or not self.libro.paginas:
            return 0
        return min(100, round((self.pagina_actual / self.libro.paginas) * 100))

    def to_dict(self):
        return {
            "id": self.id,
            "libro_id": self.libro_id,
            "titulo": self.libro.titulo if self.libro else None,
            "pagina_actual": self.pagina_actual,
            "total_paginas": self.libro.paginas if self.libro else 0,
            "porcentaje": self.porcentaje(),
            "estado": self.estado,
            "actualizado_en": (
                self.actualizado_en.isoformat() if self.actualizado_en else None
            ),
        }

    def __repr__(self):
        return f"<Progreso libro={self.libro_id} usuario={self.usuario_id}>"
