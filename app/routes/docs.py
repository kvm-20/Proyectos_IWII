"""Documentacion interactiva de la API con Swagger UI.

La pagina /docs carga Swagger UI desde su CDN y lee el contrato publicado
en /openapi.yaml, por lo que no se necesita ninguna libreria adicional.
"""

from flask import Blueprint, Response, send_file

from app.config import BASE_DIR

docs_bp = Blueprint("docs", __name__)

RUTA_CONTRATO = BASE_DIR / "docs" / "openapi.yaml"

PAGINA = """<!doctype html>
<html lang="es">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>BiblioWeb API - Documentacion</title>
    <link
      rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.17.14/swagger-ui.css"
    />
  </head>
  <body>
    <div id="swagger-ui"></div>
    <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.17.14/swagger-ui-bundle.js"></script>
    <script>
      window.ui = SwaggerUIBundle({
        url: "/openapi.yaml",
        dom_id: "#swagger-ui",
      });
    </script>
  </body>
</html>
"""


@docs_bp.get("/docs")
def pagina_documentacion():
    """Muestra la documentacion interactiva de la API."""
    return Response(PAGINA, mimetype="text/html")


@docs_bp.get("/openapi.yaml")
def contrato():
    """Entrega el contrato OpenAPI del proyecto."""
    return send_file(RUTA_CONTRATO, mimetype="application/yaml")
