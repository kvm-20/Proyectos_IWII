"""Middleware de logging: registra cada peticion con su tiempo de respuesta."""

import logging
import time

from flask import g, request

RUTAS_SILENCIOSAS = {"/metrics"}


def registrar_middleware(app):
    if not app.logger.handlers or app.logger.level == logging.NOTSET:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
        )
    app.logger.setLevel(logging.INFO)

    @app.before_request
    def iniciar_cronometro():
        g.inicio = time.perf_counter()

    @app.after_request
    def registrar_peticion(respuesta):
        duracion_ms = (time.perf_counter() - g.get("inicio", time.perf_counter())) * 1000
        respuesta.headers["X-Response-Time-ms"] = f"{duracion_ms:.1f}"
        if request.path not in RUTAS_SILENCIOSAS:
            app.logger.info(
                "%s %s -> %s (%.1f ms)",
                request.method,
                request.full_path.rstrip("?"),
                respuesta.status_code,
                duracion_ms,
            )
        return respuesta
