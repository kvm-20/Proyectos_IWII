from app import create_app
from app.extensions import db
from app.cli import cargar_datos_iniciales

app = create_app()

if __name__ == "__main__":
    # En desarrollo local crea las tablas y los datos de ejemplo automaticamente.
    with app.app_context():
        db.create_all()
        cargar_datos_iniciales()

    app.run(host="127.0.0.1", port=5000, debug=app.config["DEBUG"])
