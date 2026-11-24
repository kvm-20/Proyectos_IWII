import pytest

from app import create_app
from app.cli import cargar_datos_iniciales
from app.extensions import db


@pytest.fixture
def app():
    app = create_app("app.config.TestConfig")
    with app.app_context():
        db.create_all()
        cargar_datos_iniciales()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def _token(client, email, password):
    respuesta = client.post("/api/auth/login", json={"email": email, "password": password})
    assert respuesta.status_code == 200
    return respuesta.get_json()["access_token"]


@pytest.fixture
def admin_headers(client):
    return {"Authorization": f"Bearer {_token(client, 'admin@biblioweb.com', 'Admin123*')}"}


@pytest.fixture
def lector_headers(client):
    client.post(
        "/api/auth/register",
        json={"nombre": "Ana Prueba", "email": "ana@test.com", "password": "secreta1"},
    )
    return {"Authorization": f"Bearer {_token(client, 'ana@test.com', 'secreta1')}"}
