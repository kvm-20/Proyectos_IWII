# BiblioWeb – Biblioteca Virtual Interactiva

Proyecto final de **Ingeniería Web II** – Universidad Manuela Beltrán.
Integrantes: Karen Daniela Vargas Murcia · Alisson Dayana Carrasco Murcia.

```
                 BIBLIOWEB
                     |
        +------------+------------+
        |                         |
    FRONTEND                  BACKEND
  React + Vite        Flask (REST + JWT + ORM)
        |    REST / JSON          |
        +----------->-------------+
                                  |
                                MySQL
```

## Qué puede hacer la aplicación

1. Registrarse e iniciar sesión (recibe un **JWT**).
2. Consultar el catálogo con **búsqueda, filtros, orden y paginación**.
3. Ver el detalle de un libro con su **calificación promedio**.
4. **Leer** el libro en el navegador; el **progreso se guarda solo**.
5. Publicar **reseñas y calificaciones** (1 a 5 estrellas).
6. Manejar **Mi biblioteca**: favoritos, leyendo, leídos y pendientes.
7. Como **administrador**: crear, editar y eliminar libros.

Cuentas de prueba (se crean automáticamente):

| Rol | Correo | Contraseña |
|---|---|---|
| Administrador | admin@biblioweb.com | Admin123* |
| Lector | lector@biblioweb.com | Lector123* |

## Estructura del proyecto

```
Proyectos_IWII/
├── app/                      Backend Flask
│   ├── __init__.py           create_app (application factory)
│   ├── config.py             Configuración con variables de entorno
│   ├── extensions.py         SQLAlchemy y JWT
│   ├── models.py             Modelos ORM: Usuario, Libro, Resena, Lectura
│   ├── cli.py / seed_data.py Comando init-db y datos iniciales
│   ├── routes/               Capa HTTP (Blueprints)
│   ├── services/             Lógica de negocio y validaciones
│   ├── repositories/         Consultas a la base de datos
│   └── utils/                Errores, validación, JWT, middleware de logging
├── tests/                    Pruebas automáticas (pytest)
├── frontend/                 React + Vite (+ Dockerfile y nginx.conf)
├── docs/openapi.yaml         Contrato de la API (OpenAPI 3.0)
├── postman/                  Colección de Postman
├── monitoring/               Prometheus y Grafana
├── k8s/                      Manifiestos de Kubernetes
├── terraform/                Infraestructura como código
├── .github/workflows/ci.yml  Integración continua (GitHub Actions)
├── Dockerfile                Imagen del backend (multi-etapa)
├── docker-compose.yml        Todo el sistema con un comando
├── requirements.txt          Dependencias de producción
└── run.py                    Punto de entrada
```

---

## Paso 0. Instalar las herramientas

| Herramienta | Para qué | Verificar |
|---|---|---|
| Python 3.12 o superior | Backend | `python --version` |
| Node.js 20 o superior | Frontend | `node --version` |
| Git | Control de versiones | `git --version` |
| Docker Desktop | Contenedores y Kubernetes | `docker --version` |
| Postman | Probar la API | Abrir la aplicación |
| Terraform (opcional) | Infraestructura como código | `terraform --version` |

Copie el contenido de este proyecto dentro de su carpeta `C:\Ingenieria_Web_II\Proyectos_IWII\`.
Así conserva el historial de Git de las sesiones anteriores.

---

## Paso 1. Ejecutar en modo desarrollo (2 terminales)

En este modo el backend usa **SQLite** automáticamente, así que no necesita instalar MySQL.

**Terminal 1 – Backend (PowerShell, en la raíz del proyecto):**

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
python run.py
```

Abra http://127.0.0.1:5000/health y debe ver `"status": "ok"` y `"database": "ok"`.

**Terminal 2 – Frontend:**

```powershell
cd frontend
copy .env.example .env
npm install
npm run dev
```

Abra http://localhost:5173 y navegue por la aplicación.

> Si quiere empezar con la base de datos limpia, detenga el backend y borre la carpeta `instance/`.

---

## Paso 2. Pruebas automáticas (pytest)

Con el entorno virtual activo y en la raíz del proyecto:

```powershell
pytest
```

Resultado esperado: **29 passed**. Las pruebas usan una base de datos en memoria y cubren
registro, login, JWT, permisos (401/403), paginación, errores 400/404/409/422, filtros,
reseñas y progreso de lectura.

---

## Paso 3. Probar la API con Postman

1. Con el backend encendido, abra Postman → **Import** → seleccione `postman/BiblioWeb.postman_collection.json`.
2. Clic derecho en la colección → **Run collection** → **Run BiblioWeb API**.
3. Resultado esperado: 28 peticiones y 36 pruebas en verde.

La colección guarda el token automáticamente después del login (variables `token` y `adminToken`).

---

## Paso 4. Ejecutar todo con Docker

Abra Docker Desktop y espere a que diga *Engine running*. Detenga los servidores del Paso 1 (Ctrl + C).

```powershell
copy .env.example .env        # edite las claves si quiere
docker compose up -d --build
docker compose ps
```

| Servicio | Dirección |
|---|---|
| Aplicación (React + Nginx) | http://localhost:8080 |
| API Flask | http://localhost:5000/health |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 (usuario y clave del `.env`) |
| MySQL | localhost:3307 |

La primera vez tarda unos minutos porque descarga las imágenes. Para ver los logs del backend
(incluye el middleware de logging): `docker compose logs -f backend`.

Para apagar todo: `docker compose down` (agregue `-v` para borrar también los datos).

---

## Paso 5. Métricas con Prometheus y Grafana

1. Use la aplicación en http://localhost:8080 por un minuto (abra libros, busque, inicie sesión).
2. Prometheus: http://localhost:9090 → **Status → Targets**: `biblioweb-backend` debe estar **UP**.
3. Grafana: http://localhost:3000 → **Dashboards → BiblioWeb → BiblioWeb - Backend Flask**.
   Verá peticiones por segundo, latencia p95, errores y respuestas por código HTTP.

El backend publica las métricas en http://localhost:5000/metrics.

---

## Paso 6. Desplegar en Kubernetes (Docker Desktop)

1. Docker Desktop → **Settings → Kubernetes → Enable Kubernetes** → *Apply & restart*.
2. Construya las imágenes (si no lo hizo en el Paso 4): `docker compose build backend frontend`
3. Despliegue:

```powershell
kubectl apply -f k8s/00-namespace.yaml
kubectl create secret generic biblioweb-secret --from-env-file=.env -n biblioweb
kubectl apply -f k8s/
kubectl get pods -n biblioweb -w
```

Espere a que todos los pods estén `Running` y `READY 1/1` (Ctrl + C para salir).
Abra http://localhost:30080.

Comandos útiles para la sustentación:

```powershell
kubectl get all -n biblioweb
kubectl scale deployment backend --replicas=3 -n biblioweb
kubectl logs deployment/backend -n biblioweb
kubectl delete namespace biblioweb     # borrar todo
```

> Si tiene `docker compose` encendido al mismo tiempo no hay conflicto: Kubernetes usa el puerto 30080.

---

## Paso 7. Infraestructura como código con Terraform

Terraform crea la red, el volumen y los contenedores con el proveedor de Docker.

```powershell
docker compose down                     # libera recursos
docker compose build backend frontend   # imágenes que usará Terraform
cd terraform
copy terraform.tfvars.example terraform.tfvars
terraform init
terraform plan
terraform apply                         # escriba: yes
```

Abra http://localhost:8081. Para destruir lo creado: `terraform destroy`.

---

## Paso 8. Integración continua con GitHub Actions

```powershell
git add .
git commit -m "Proyecto final BiblioWeb: API completa, React, pruebas, Docker, K8s, CI, Terraform y monitoreo"
git push
```

En GitHub → pestaña **Actions** verá el workflow **CI BiblioWeb** con tres trabajos:
pruebas del backend (pytest), build del frontend y construcción de las imágenes Docker.

---

## Endpoints de la API

| Verbo | Ruta | Auth | Respuestas |
|---|---|---|---|
| GET | /health | – | 200 |
| POST | /api/auth/register | – | 201, 400, 409, 422 |
| POST | /api/auth/login | – | 200, 401, 422 |
| GET | /api/auth/me | JWT | 200, 401 |
| GET | /api/libros?q=&categoria=&orden=&direccion=&page=&limit= | – | 200, 400 |
| GET | /api/libros/categorias | – | 200 |
| GET | /api/libros/{id} | – | 200, 404 |
| GET | /api/libros/{id}/contenido | JWT | 200, 401, 404 |
| POST | /api/libros | Admin | 201, 401, 403, 409, 422 |
| PUT | /api/libros/{id} | Admin | 200, 403, 404, 422 |
| DELETE | /api/libros/{id} | Admin | 204, 403, 404 |
| GET | /api/libros/{id}/resenas?min=&orden= | – | 200, 400, 404 |
| POST | /api/libros/{id}/resenas | JWT | 201, 401, 409, 422 |
| DELETE | /api/resenas/{id} | Dueño o admin | 204, 403, 404 |
| GET | /api/mi-biblioteca?estado=&favorito= | JWT | 200, 400, 401 |
| PUT | /api/mi-biblioteca/{id} | JWT | 200, 404, 422 |
| DELETE | /api/mi-biblioteca/{id} | JWT | 204, 404 |

El contrato completo está en `docs/openapi.yaml` (puede pegarlo en https://editor.swagger.io).

## Problemas comunes

| Problema | Solución |
|---|---|
| `Activate.ps1 no se puede cargar` | Ejecute antes `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` |
| El frontend dice "Backend sin conexión" | Verifique que `python run.py` esté corriendo y que exista `frontend/.env` |
| `port is already allocated` en Docker | Otro programa usa ese puerto; cierre el Paso 1 o cambie el puerto en `docker-compose.yml` |
| El backend en Docker reinicia | Espere: está esperando a que MySQL arranque (`docker compose logs backend`) |
| Pods en `ErrImageNeverPull` o `ImagePullBackOff` | Ejecute `docker compose build backend frontend` antes de `kubectl apply` |
| Terraform no conecta con Docker | En Linux/Mac ponga `docker_host = "unix:///var/run/docker.sock"` en `terraform.tfvars` |
