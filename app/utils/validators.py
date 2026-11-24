"""Validacion y limpieza de los datos que llegan desde el cliente.

Regla de seguridad aplicada: nunca se confia en la entrada del usuario.
Todo dato se valida en el servidor, aunque el formulario de React ya lo
haya validado antes.
"""

import re

from app.utils.errors import ErrorAPI

PATRON_CORREO = re.compile(r"^[^@\s]+@[^@\s]+\.[a-zA-Z]{2,}$")
PATRON_ETIQUETAS = re.compile(r"<[^>]*>")


def limpiar_texto(valor):
    """Quita espacios sobrantes y cualquier etiqueta HTML del texto.

    Es una defensa adicional contra XSS almacenado: aunque React escapa el
    contenido al renderizarlo, el dato se guarda ya limpio en la base.
    """
    if valor is None:
        return ""
    return PATRON_ETIQUETAS.sub("", str(valor)).strip()


def validar_obligatorio(valor, campo, maximo=200):
    texto = limpiar_texto(valor)
    if not texto:
        raise ErrorAPI(f"El campo '{campo}' es obligatorio")
    if len(texto) > maximo:
        raise ErrorAPI(f"El campo '{campo}' supera los {maximo} caracteres")
    return texto


def validar_correo(valor):
    correo = limpiar_texto(valor).lower()
    if not PATRON_CORREO.match(correo):
        raise ErrorAPI("El correo electronico no tiene un formato valido")
    return correo


def validar_contrasena(valor):
    if not valor or len(valor) < 8:
        raise ErrorAPI("La contrasena debe tener al menos 8 caracteres")
    if not re.search(r"[A-Za-z]", valor) or not re.search(r"\d", valor):
        raise ErrorAPI("La contrasena debe combinar letras y numeros")
    return valor


def validar_calificacion(valor):
    try:
        calificacion = int(valor)
    except (TypeError, ValueError):
        raise ErrorAPI("La calificacion debe ser un numero entero")
    if calificacion < 1 or calificacion > 5:
        raise ErrorAPI("La calificacion debe estar entre 1 y 5")
    return calificacion


def validar_entero(valor, campo, minimo=0):
    try:
        numero = int(valor)
    except (TypeError, ValueError):
        raise ErrorAPI(f"El campo '{campo}' debe ser un numero entero")
    if numero < minimo:
        raise ErrorAPI(f"El campo '{campo}' no puede ser menor que {minimo}")
    return numero
