def test_registro_exitoso_devuelve_201(client):
    respuesta = client.post(
        "/api/auth/register",
        json={"nombre": "Karen", "email": "karen@test.com", "password": "clave123"},
    )
    assert respuesta.status_code == 201
    usuario = respuesta.get_json()["usuario"]
    assert usuario["email"] == "karen@test.com"
    assert usuario["rol"] == "lector"
    assert "password" not in usuario and "password_hash" not in usuario


def test_registro_sin_json_devuelve_400(client):
    respuesta = client.post("/api/auth/register", data="texto plano")
    assert respuesta.status_code == 400


def test_registro_con_datos_invalidos_devuelve_422(client):
    respuesta = client.post(
        "/api/auth/register", json={"nombre": "A", "email": "no-es-correo", "password": "123"}
    )
    assert respuesta.status_code == 422
    detalles = respuesta.get_json()["error"]["detalles"]
    assert set(detalles) == {"nombre", "email", "password"}


def test_registro_con_email_repetido_devuelve_409(client):
    datos = {"nombre": "Karen", "email": "repetido@test.com", "password": "clave123"}
    client.post("/api/auth/register", json=datos)
    assert client.post("/api/auth/register", json=datos).status_code == 409


def test_login_devuelve_jwt(client):
    respuesta = client.post(
        "/api/auth/login", json={"email": "admin@biblioweb.com", "password": "Admin123*"}
    )
    assert respuesta.status_code == 200
    datos = respuesta.get_json()
    assert datos["access_token"].count(".") == 2  # formato JWT: header.payload.firma
    assert datos["usuario"]["rol"] == "admin"


def test_login_con_clave_incorrecta_devuelve_401(client):
    respuesta = client.post(
        "/api/auth/login", json={"email": "admin@biblioweb.com", "password": "mala"}
    )
    assert respuesta.status_code == 401


def test_me_requiere_token(client, lector_headers):
    assert client.get("/api/auth/me").status_code == 401
    respuesta = client.get("/api/auth/me", headers=lector_headers)
    assert respuesta.status_code == 200
    assert respuesta.get_json()["email"] == "ana@test.com"
