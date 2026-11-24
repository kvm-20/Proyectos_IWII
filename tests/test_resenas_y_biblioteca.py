def test_crear_resena_actualiza_promedio(client, lector_headers):
    respuesta = client.post(
        "/api/libros/6/resenas",
        json={"calificacion": 4, "comentario": "Muy buena"},
        headers=lector_headers,
    )
    assert respuesta.status_code == 201
    libro = client.get("/api/libros/6").get_json()
    assert libro["total_resenas"] == 1
    assert libro["calificacion_promedio"] == 4.0


def test_resena_requiere_sesion_y_calificacion_valida(client, lector_headers):
    assert client.post("/api/libros/6/resenas", json={"calificacion": 5}).status_code == 401
    respuesta = client.post("/api/libros/6/resenas", json={"calificacion": 9}, headers=lector_headers)
    assert respuesta.status_code == 422


def test_resena_duplicada_devuelve_409(client, lector_headers):
    client.post("/api/libros/6/resenas", json={"calificacion": 5}, headers=lector_headers)
    respuesta = client.post("/api/libros/6/resenas", json={"calificacion": 3}, headers=lector_headers)
    assert respuesta.status_code == 409


def test_filtrar_resenas_por_calificacion_minima(client, lector_headers, admin_headers):
    client.post("/api/libros/6/resenas", json={"calificacion": 2}, headers=lector_headers)
    client.post("/api/libros/6/resenas", json={"calificacion": 5}, headers=admin_headers)
    items = client.get("/api/libros/6/resenas?min=4").get_json()["items"]
    assert [r["calificacion"] for r in items] == [5]


def test_solo_el_dueno_puede_borrar_su_resena(client, lector_headers, admin_headers):
    resena_id = client.post(
        "/api/libros/6/resenas", json={"calificacion": 5}, headers=admin_headers
    ).get_json()["id"]
    assert client.delete(f"/api/resenas/{resena_id}", headers=lector_headers).status_code == 403
    assert client.delete(f"/api/resenas/{resena_id}", headers=admin_headers).status_code == 204


def test_progreso_de_lectura_y_listas(client, lector_headers):
    respuesta = client.put(
        "/api/mi-biblioteca/1",
        json={"pagina_actual": 1, "total_paginas": 3, "favorito": True},
        headers=lector_headers,
    )
    assert respuesta.status_code == 200
    lectura = respuesta.get_json()
    assert lectura["estado"] == "leyendo"
    assert lectura["porcentaje"] == 33

    terminado = client.put(
        "/api/mi-biblioteca/1", json={"pagina_actual": 3}, headers=lector_headers
    ).get_json()
    assert terminado["estado"] == "leido"
    assert terminado["porcentaje"] == 100

    favoritos = client.get("/api/mi-biblioteca?favorito=true", headers=lector_headers).get_json()
    assert [l["libro"]["id"] for l in favoritos] == [1]

    assert client.delete("/api/mi-biblioteca/1", headers=lector_headers).status_code == 204
    assert client.get("/api/mi-biblioteca", headers=lector_headers).get_json() == []


def test_estado_invalido_en_biblioteca_devuelve_422(client, lector_headers):
    respuesta = client.put("/api/mi-biblioteca/1", json={"estado": "olvidado"}, headers=lector_headers)
    assert respuesta.status_code == 422
