"""Modelo Resena: calificacion y comentario de un lector sobre un libro."""

from datetime import datetime, timezone

from app.extensions import db


class Resena(db.Model):
    """Una resena por usuario y por libro."""

    __tablename__ = "resenas"
    __table_args__ = (
        db.UniqueConstraint("libro_id", "usuario_id", name="uq_resena_libro_usuario"),
    )

    id = db.Column(db.Integer, primary_key=True)
    libro_id = db.Column(
        db.Integer, db.ForeignKey("libros.id", ondelete="CASCADE"), nullable=False
    )
    usuario_id = db.Column(
        db.Integer, db.ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False
    )
    calificacion = db.Column(db.Integer, nullable=False)
    comentario = db.Column(db.Text)
    creada_en = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    libro = db.relationship("Libro", back_populates="resenas")
    usuario = db.relationship("Usuario", back_populates="resenas")

    def to_dict(self):
        return {
            "id": self.id,
            "libro_id": self.libro_id,
            "usuario_id": self.usuario_id,
            "usuario": self.usuario.nombre if self.usuario else None,
            "calificacion": self.calificacion,
            "comentario": self.comentario,
            "creada_en": self.creada_en.isoformat() if self.creada_en else None,
        }

    def __repr__(self):
        return f"<Resena libro={self.libro_id} usuario={self.usuario_id}>"
