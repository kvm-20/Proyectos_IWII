def test_health_responde_ok(client):
    respuesta = client.get("/health")
    assert respuesta.status_code == 200
    datos = respuesta.get_json()
    assert datos["status"] == "ok"
    assert datos["database"] == "ok"


def test_ruta_inexistente_devuelve_404_en_json(client):
    respuesta = client.get("/api/no-existe")
    assert respuesta.status_code == 404
    assert respuesta.get_json()["error"]["codigo"] == 404


def test_middleware_agrega_tiempo_de_respuesta(client):
    respuesta = client.get("/health")
    assert "X-Response-Time-ms" in respuesta.headers
