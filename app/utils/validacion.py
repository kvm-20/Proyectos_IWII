"""Funciones auxiliares para leer y validar los datos de las peticiones."""

import re

from flask import request

from app.utils.errores import ApiError

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def leer_json():
    """Devuelve el cuerpo JSON o lanza 400 si no es JSON valido."""
    datos = request.get_json(silent=True)
    if not isinstance(datos, dict):
        raise ApiError("El cuerpo de la petición debe ser un objeto JSON", 400)
    return datos


def lanzar_si_hay_errores(errores):
    """Si hay errores de validacion de datos responde 422 con el detalle por campo."""
    if errores:
        raise ApiError("Los datos enviados no son válidos", 422, errores)


def texto(datos, campo, errores, requerido=True, minimo=1, maximo=255):
    valor = datos.get(campo)
    if valor is None or (isinstance(valor, str) and not valor.strip()):
        if requerido:
            errores[campo] = "Este campo es obligatorio"
        return None
    if not isinstance(valor, str):
        errores[campo] = "Debe ser texto"
        return None
    valor = valor.strip()
    if len(valor) < minimo:
        errores[campo] = f"Debe tener al menos {minimo} caracteres"
    elif len(valor) > maximo:
        errores[campo] = f"Debe tener máximo {maximo} caracteres"
    return valor


def entero(datos, campo, errores, requerido=True, minimo=None, maximo=None):
    valor = datos.get(campo)
    if valor is None or valor == "":
        if requerido:
            errores[campo] = "Este campo es obligatorio"
        return None
    if isinstance(valor, bool):
        errores[campo] = "Debe ser un número entero"
        return None
    try:
        valor = int(valor)
    except (TypeError, ValueError):
        errores[campo] = "Debe ser un número entero"
        return None
    if minimo is not None and valor < minimo:
        errores[campo] = f"Debe ser mayor o igual a {minimo}"
    elif maximo is not None and valor > maximo:
        errores[campo] = f"Debe ser menor o igual a {maximo}"
    return valor


def email(datos, campo, errores):
    valor = texto(datos, campo, errores, maximo=120)
    if valor and not EMAIL_RE.match(valor):
        errores[campo] = "El correo no tiene un formato válido"
    return valor.lower() if valor else valor


def parametro_entero(nombre, defecto, minimo=1, maximo=None):
    """Lee un parametro de la URL (?page=2). Si no es numero responde 400."""
    crudo = request.args.get(nombre)
    if crudo is None or crudo == "":
        return defecto
    try:
        valor = int(crudo)
    except ValueError:
        raise ApiError(f"El parametro '{nombre}' debe ser un número entero", 400)
    if valor < minimo:
        raise ApiError(f"El parametro '{nombre}' debe ser mayor o igual a {minimo}", 400)
    if maximo is not None and valor > maximo:
        valor = maximo
    return valor


def leer_paginacion(limite_defecto=8, limite_maximo=50):
    page = parametro_entero("page", 1)
    limit = parametro_entero("limit", limite_defecto, maximo=limite_maximo)
    return page, limit


def respuesta_paginada(items, total, page, limit):
    paginas = (total + limit - 1) // limit if total else 0
    return {
        "items": items,
        "paginacion": {
            "page": page,
            "limit": limit,
            "total": total,
            "paginas": paginas,
            "tiene_siguiente": page < paginas,
            "tiene_anterior": page > 1,
        },
    }
