"""Manejo centralizado de errores de la API.

Gracias a estos manejadores la API siempre responde en JSON, incluso cuando
ocurre un error. Asi el frontend nunca recibe una pagina HTML inesperada.
"""

from flask import jsonify


class ErrorAPI(Exception):
    """Error controlado que la API devuelve al cliente."""

    def __init__(self, mensaje, codigo=400):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.codigo = codigo


def registrar_manejadores(app):
    """Asocia los manejadores de error a la aplicacion Flask."""

    @app.errorhandler(ErrorAPI)
    def _error_api(error):
        return jsonify({"error": error.mensaje}), error.codigo

    @app.errorhandler(400)
    def _solicitud_invalida(_error):
        return jsonify({"error": "Solicitud invalida"}), 400

    @app.errorhandler(401)
    def _no_autenticado(_error):
        return jsonify({"error": "Se requiere iniciar sesion"}), 401

    @app.errorhandler(403)
    def _sin_permiso(_error):
        return jsonify({"error": "No tiene permisos para esta operacion"}), 403

    @app.errorhandler(404)
    def _no_encontrado(_error):
        return jsonify({"error": "Recurso no encontrado"}), 404

    @app.errorhandler(405)
    def _metodo_no_permitido(_error):
        return jsonify({"error": "Metodo no permitido"}), 405

    @app.errorhandler(500)
    def _error_interno(_error):
        # No se expone la traza al cliente: podria revelar rutas internas.
        return jsonify({"error": "Error interno del servidor"}), 500
