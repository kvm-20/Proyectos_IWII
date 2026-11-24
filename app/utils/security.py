"""Cabeceras de seguridad HTTP aplicadas a todas las respuestas.

Cada cabecera mitiga un riesgo concreto del OWASP Top 10 2021.
"""

from flask import request

CABECERAS = {
    # Evita que el navegador adivine el tipo de contenido (ataques MIME).
    "X-Content-Type-Options": "nosniff",
    # Impide que la API se cargue dentro de un iframe (clickjacking).
    "X-Frame-Options": "DENY",
    # Limita la informacion de origen que se envia a otros sitios.
    "Referrer-Policy": "no-referrer",
    # Desactiva APIs del navegador que la API no necesita.
    "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
}

# La API solo devuelve JSON: se bloquea la carga de cualquier recurso.
CSP_API = "default-src 'none'; frame-ancestors 'none'"

# La pagina /docs si necesita cargar Swagger UI desde su CDN.
CSP_DOCS = (
    "default-src 'self'; "
    "script-src 'self' https://cdn.jsdelivr.net 'unsafe-inline'; "
    "style-src 'self' https://cdn.jsdelivr.net 'unsafe-inline'; "
    "img-src 'self' data:; "
    "connect-src 'self'; "
    "frame-ancestors 'none'"
)


def registrar_cabeceras(app):
    """Agrega las cabeceras de seguridad a cada respuesta de la API."""

    @app.after_request
    def _aplicar_cabeceras(respuesta):
        for nombre, valor in CABECERAS.items():
            respuesta.headers.setdefault(nombre, valor)

        politica = CSP_DOCS if request.path.startswith("/docs") else CSP_API
        respuesta.headers.setdefault("Content-Security-Policy", politica)
        return respuesta
