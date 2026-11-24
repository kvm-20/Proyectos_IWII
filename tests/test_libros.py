NUEVO_LIBRO = {
    "titulo": "La vorágine",
    "autor": "José Eustasio Rivera",
    "categoria": "Novela",
    "anio": 1924,
    "descripcion": "Novela colombiana sobre la selva y la explotación del caucho.",
    "contenido": "Pagina uno.\n\nPagina dos.",
}


def test_listar_libros_con_paginacion(client):
    respuesta = client.get("/api/libros?page=1&limit=3")
    assert respuesta.status_code == 200
    datos = respuesta.get_json()
    assert len(datos["items"]) == 3
    assert datos["paginacion"]["total"] == 7
    assert datos["paginacion"]["paginas"] == 3
    assert datos["paginacion"]["tiene_siguiente"] is True


def test_paginacion_con_parametro_no_numerico_devuelve_400(client):
    assert client.get("/api/libros?page=abc").status_code == 400


def test_filtrar_por_categoria_y_buscar_por_texto(client):
    novelas = client.get("/api/libros?categoria=Novela").get_json()["items"]
    assert novelas and all(libro["categoria"] == "Novela" for libro in novelas)

    busqueda = client.get("/api/libros?q=cervantes").get_json()["items"]
    assert [libro["titulo"] for libro in busqueda] == ["Don Quijote de la Mancha"]


def test_ordenar_por_calificacion_descendente(client):
    items = client.get("/api/libros?orden=calificacion&direccion=desc").get_json()["items"]
    promedios = [libro["calificacion_promedio"] for libro in items]
    assert promedios == sorted(promedios, reverse=True)


def test_orden_invalido_devuelve_400(client):
    assert client.get("/api/libros?orden=precio").status_code == 400


def test_libro_inexistente_devuelve_404(client):
    assert client.get("/api/libros/9999").status_code == 404


def test_contenido_requiere_sesion(client, lector_headers):
    assert client.get("/api/libros/1/contenido").status_code == 401
    respuesta = client.get("/api/libros/1/contenido", headers=lector_headers)
    assert respuesta.status_code == 200
    assert respuesta.get_json()["contenido"]


def test_crear_libro_requiere_admin(client, lector_headers, admin_headers):
    assert client.post("/api/libros", json=NUEVO_LIBRO).status_code == 401
    assert client.post("/api/libros", json=NUEVO_LIBRO, headers=lector_headers).status_code == 403

    respuesta = client.post("/api/libros", json=NUEVO_LIBRO, headers=admin_headers)
    assert respuesta.status_code == 201
    assert respuesta.get_json()["titulo"] == "La vorágine"


def test_crear_libro_duplicado_devuelve_409(client, admin_headers):
    client.post("/api/libros", json=NUEVO_LIBRO, headers=admin_headers)
    assert client.post("/api/libros", json=NUEVO_LIBRO, headers=admin_headers).status_code == 409


def test_crear_libro_invalido_devuelve_422(client, admin_headers):
    respuesta = client.post("/api/libros", json={"titulo": "", "anio": "hace mucho"}, headers=admin_headers)
    assert respuesta.status_code == 422
    detalles = respuesta.get_json()["error"]["detalles"]
    assert {"titulo", "autor", "categoria", "anio"} <= set(detalles)


def test_actualizar_y_eliminar_libro(client, admin_headers):
    libro_id = client.post("/api/libros", json=NUEVO_LIBRO, headers=admin_headers).get_json()["id"]

    respuesta = client.put(f"/api/libros/{libro_id}", json={"anio": 1925}, headers=admin_headers)
    assert respuesta.status_code == 200
    assert respuesta.get_json()["anio"] == 1925

    assert client.delete(f"/api/libros/{libro_id}", headers=admin_headers).status_code == 204
    assert client.get(f"/api/libros/{libro_id}").status_code == 404


def test_listar_categorias(client):
    categorias = client.get("/api/libros/categorias").get_json()
    assert "Novela" in categorias
