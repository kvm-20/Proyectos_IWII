from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.services import libro_service, resena_service
from app.utils.seguridad import admin_requerido, es_admin, usuario_actual_id
from app.utils.validacion import (
    leer_json,
    leer_paginacion,
    parametro_entero,
    respuesta_paginada,
)

libros_bp = Blueprint("libros", __name__, url_prefix="/api")


# ---------- Catalogo (publico) ----------

@libros_bp.get("/libros")
def listar_libros():
    """GET /api/libros?q=&categoria=&autor=&orden=&direccion=&page=&limit="""
    page, limit = leer_paginacion()
    items, total = libro_service.listar(request.args, page, limit)
    return jsonify(respuesta_paginada(items, total, page, limit))


@libros_bp.get("/libros/categorias")
def listar_categorias():
    return jsonify(libro_service.categorias())


@libros_bp.get("/libros/<int:libro_id>")
def obtener_libro(libro_id):
    return jsonify(libro_service.obtener(libro_id))


@libros_bp.get("/libros/<int:libro_id>/contenido")
@jwt_required()
def leer_libro(libro_id):
    """El contenido para el visor de lectura solo esta disponible con sesion iniciada."""
    return jsonify(libro_service.obtener(libro_id, incluir_contenido=True))


# ---------- Administracion del catalogo (solo admin) ----------

@libros_bp.post("/libros")
@admin_requerido
def crear_libro():
    return jsonify(libro_service.crear(leer_json())), 201


@libros_bp.put("/libros/<int:libro_id>")
@admin_requerido
def actualizar_libro(libro_id):
    return jsonify(libro_service.actualizar(libro_id, leer_json()))


@libros_bp.delete("/libros/<int:libro_id>")
@admin_requerido
def eliminar_libro(libro_id):
    libro_service.eliminar(libro_id)
    return "", 204


# ---------- Resenas ----------

@libros_bp.get("/libros/<int:libro_id>/resenas")
def listar_resenas(libro_id):
    """GET /api/libros/1/resenas?min=4&orden=calificacion&page=1&limit=10"""
    page, limit = leer_paginacion(limite_defecto=10)
    minimo = parametro_entero("min", None, minimo=1, maximo=5)
    orden = request.args.get("orden", "recientes")
    items, total = resena_service.listar(libro_id, minimo, orden, page, limit)
    return jsonify(respuesta_paginada(items, total, page, limit))


@libros_bp.post("/libros/<int:libro_id>/resenas")
@jwt_required()
def crear_resena(libro_id):
    resena = resena_service.crear(libro_id, usuario_actual_id(), leer_json())
    return jsonify(resena), 201


@libros_bp.delete("/resenas/<int:resena_id>")
@jwt_required()
def eliminar_resena(resena_id):
    resena_service.eliminar(resena_id, usuario_actual_id(), es_admin())
    return "", 204
