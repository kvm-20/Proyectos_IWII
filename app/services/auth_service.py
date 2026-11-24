"""Logica de negocio de registro e inicio de sesion."""

from flask_jwt_extended import create_access_token

from app.models import Usuario
from app.repositories import usuario_repository
from app.utils import validacion as v
from app.utils.errores import ApiError


def registrar(datos):
    errores = {}
    nombre = v.texto(datos, "nombre", errores, minimo=2, maximo=100)
    email = v.email(datos, "email", errores)
    password = v.texto(datos, "password", errores, minimo=6, maximo=128)
    v.lanzar_si_hay_errores(errores)

    if usuario_repository.buscar_por_email(email):
        raise ApiError("Ya existe un usuario registrado con ese correo", 409)

    usuario = Usuario(nombre=nombre, email=email, rol="lector")
    usuario.set_password(password)
    return usuario_repository.guardar(usuario)


def generar_token(usuario):
    return create_access_token(
        identity=str(usuario.id),
        additional_claims={"rol": usuario.rol, "nombre": usuario.nombre},
    )


def iniciar_sesion(datos):
    errores = {}
    email = v.email(datos, "email", errores)
    password = v.texto(datos, "password", errores, maximo=128)
    v.lanzar_si_hay_errores(errores)

    usuario = usuario_repository.buscar_por_email(email)
    if not usuario or not usuario.check_password(password):
        raise ApiError("Correo o contraseña incorrectos", 401)

    return {"access_token": generar_token(usuario), "usuario": usuario.to_dict()}
