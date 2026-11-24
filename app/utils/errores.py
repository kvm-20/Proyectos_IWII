"""Manejo centralizado de errores: todas las respuestas de error son JSON.

Convencion usada en la API:
  400 Bad Request          -> la peticion esta mal formada (no es JSON, parametro no numerico).
  401 Unauthorized         -> falta el token JWT o es invalido.
  403 Forbidden            -> el usuario no tiene permiso (no es admin / no es el dueno).
  404 Not Found            -> el recurso no existe.
  409 Conflict             -> el recurso ya existe (email repetido, resena duplicada).
  422 Unprocessable Entity -> el JSON es valido pero los datos no cumplen las reglas.
"""

from flask import jsonify
from werkzeug.exceptions import HTTPException


class ApiError(Exception):
    def __init__(self, mensaje, status=400, detalles=None):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.status = status
        self.detalles = detalles


def respuesta_error(mensaje, status, detalles=None):
    cuerpo = {"error": {"codigo": status, "mensaje": mensaje}}
    if detalles:
        cuerpo["error"]["detalles"] = detalles
    return jsonify(cuerpo), status


def registrar_manejadores(app):
    @app.errorhandler(ApiError)
    def manejar_api_error(error):
        return respuesta_error(error.mensaje, error.status, error.detalles)

    @app.errorhandler(HTTPException)
    def manejar_http(error):
        mensajes = {
            404: "Recurso no encontrado",
            405: "Método HTTP no permitido para esta ruta",
        }
        return respuesta_error(mensajes.get(error.code, error.description), error.code)

    @app.errorhandler(Exception)
    def manejar_inesperado(error):
        app.logger.exception("Error no controlado: %s", error)
        return respuesta_error("Error interno del servidor", 500)
