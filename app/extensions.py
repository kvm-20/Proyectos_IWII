"""Extensiones de Flask creadas una sola vez y conectadas en create_app."""

from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
jwt = JWTManager()
