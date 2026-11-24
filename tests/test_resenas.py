"""Pruebas de resenas, calificaciones y progreso de lectura."""

from tests.conftest import autenticar


def test_publicar_resena_requiere_sesion(client, libro):
    respuesta = client.post(
        f"/api/libros/{libro.id}/resenas", json={"calificacion": 5}
    )

    assert respuesta.status_code == 401


def test_publicar_resena(client, libro, usuario_lector):
    cabeceras = autenticar(client, "lectora@test.com", "prueba2026")

    respuesta = client.post(
        f"/api/libros/{libro.id}/resenas",
        headers=cabeceras,
        json={"calificacion": 4, "comentario": "Muy buena lectura"},
    )

    assert respuesta.status_code == 201
    assert respuesta.get_json()["calificacion"] == 4


def test_rechaza_calificacion_fuera_de_rango(client, libro, usuario_lector):
    cabeceras = autenticar(client, "lectora@test.com", "prueba2026")

    respuesta = client.post(
        f"/api/libros/{libro.id}/resenas",
        headers=cabeceras,
        json={"calificacion": 9},
    )

    assert respuesta.status_code == 400


def test_el_comentario_se_guarda_sin_etiquetas_html(client, libro, usuario_lector):
    """Defensa contra XSS almacenado: el script no debe quedar en la base."""
    cabeceras = autenticar(client, "lectora@test.com", "prueba2026")

    respuesta = client.post(
        f"/api/libros/{libro.id}/resenas",
        headers=cabeceras,
        json={
            "calificacion": 5,
            "comentario": "Excelente <script>alert('xss')</script>",
        },
    )

    assert "<script>" not in respuesta.get_json()["comentario"]


def test_actualizar_progreso_de_lectura(client, libro, usuario_lector):
    cabeceras = autenticar(client, "lectora@test.com", "prueba2026")

    respuesta = client.put(
        f"/api/libros/{libro.id}/progreso",
        headers=cabeceras,
        json={"pagina_actual": 50, "estado": "leyendo"},
    )

    assert respuesta.status_code == 200
    assert respuesta.get_json()["porcentaje"] == 50


def test_no_permite_una_pagina_mayor_al_total(client, libro, usuario_lector):
    cabeceras = autenticar(client, "lectora@test.com", "prueba2026")

    respuesta = client.put(
        f"/api/libros/{libro.id}/progreso",
        headers=cabeceras,
        json={"pagina_actual": 5000},
    )

    assert respuesta.status_code == 400
