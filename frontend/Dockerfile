# ============================================================
# Frontend BiblioWeb (React + Vite) - construccion multi-etapa
# ============================================================

# ---- Etapa 1: compilar React a archivos estaticos ----
FROM node:22-alpine AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
# Vacio = el navegador llama a /api en el mismo dominio y Nginx lo envia al backend
ARG VITE_API_URL=""
ENV VITE_API_URL=${VITE_API_URL}
RUN npm run build

# ---- Etapa 2: servir solo los archivos compilados con Nginx ----
FROM nginx:1.27-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
