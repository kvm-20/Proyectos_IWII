"""Modelo Usuario: lectores y administradores de la plataforma."""

from datetime import datetime, timezone

from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db


class Usuario(db.Model):
    """Representa a una persona registrada en BiblioWeb."""

    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False, index=True)
    contrasena_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(20), nullable=False, default="lector")
    creado_en = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    resenas = db.relationship(
        "Resena", back_populates="usuario", cascade="all, delete-orphan"
    )
    progresos = db.relationship(
        "Progreso", back_populates="usuario", cascade="all, delete-orphan"
    )

    def definir_contrasena(self, contrasena):
        """Guarda la contrasena como hash; nunca se almacena en texto plano."""
        self.contrasena_hash = generate_password_hash(contrasena)

    def verificar_contrasena(self, contrasena):
        """Compara una contrasena recibida contra el hash almacenado."""
        return check_password_hash(self.contrasena_hash, contrasena)

    def es_admin(self):
        return self.rol == "admin"

    def to_dict(self):
        """Representacion publica del usuario (sin datos sensibles)."""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "correo": self.correo,
            "rol": self.rol,
        }

    def __repr__(self):
        return f"<Usuario {self.correo}>"
