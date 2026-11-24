# ============================================================
# Backend BiblioWeb (Flask) - construccion multi-etapa
# ============================================================

# ---- Etapa 1: compilar las dependencias como wheels ----
FROM python:3.12-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
 && pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# ---- Etapa 2: imagen final liviana (sin herramientas de compilacion) ----
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_DEBUG=false
WORKDIR /app

# Usuario sin privilegios (buena practica de seguridad)
RUN useradd --create-home --uid 1000 appuser

COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels

COPY app ./app
COPY run.py .
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 5000
HEALTHCHECK --interval=15s --timeout=5s --start-period=30s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/health')"

# 1) Crea tablas y datos iniciales (espera a MySQL)  2) Arranca Gunicorn
CMD ["sh", "-c", "flask --app run.py init-db && gunicorn --workers 1 --threads 4 --bind 0.0.0.0:5000 --access-logfile - run:app"]
