"""Modelo Libro: cada obra disponible en el catalogo."""

from datetime import datetime, timezone

from app.extensions import db


class Libro(db.Model):
    """Representa un libro del catalogo de BiblioWeb."""

    __tablename__ = "libros"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False, index=True)
    autor = db.Column(db.String(150), nullable=False, index=True)
    categoria = db.Column(db.String(80), nullable=False, index=True)
    anio = db.Column(db.Integer)
    descripcion = db.Column(db.Text)
    paginas = db.Column(db.Integer, default=0)
    formato = db.Column(db.String(10), default="PDF")
    archivo_url = db.Column(db.String(300))
    creado_en = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    resenas = db.relationship(
        "Resena", back_populates="libro", cascade="all, delete-orphan"
    )
    progresos = db.relationship(
        "Progreso", back_populates="libro", cascade="all, delete-orphan"
    )

    def calificacion_promedio(self):
        """Promedio de las calificaciones recibidas, redondeado a un decimal."""
        if not self.resenas:
            return 0.0
        total = sum(resena.calificacion for resena in self.resenas)
        return round(total / len(self.resenas), 1)

    def to_dict(self, incluir_resenas=False):
        datos = {
            "id": self.id,
            "titulo": self.titulo,
            "autor": self.autor,
            "categoria": self.categoria,
            "anio": self.anio,
            "descripcion": self.descripcion,
            "paginas": self.paginas,
            "formato": self.formato,
            "archivo_url": self.archivo_url,
            "calificacion_promedio": self.calificacion_promedio(),
            "total_resenas": len(self.resenas),
        }
        if incluir_resenas:
            datos["resenas"] = [resena.to_dict() for resena in self.resenas]
        return datos

    def __repr__(self):
        return f"<Libro {self.titulo}>"
