// Toda la comunicación con el backend está centralizada en este archivo.
// En desarrollo VITE_API_URL apunta a Flask (http://127.0.0.1:5000).
// En Docker/Kubernetes queda vacía y Nginx redirige /api al backend.
const API_URL = import.meta.env.VITE_API_URL || "";

const CLAVE_TOKEN = "biblioweb_token";

export const sesion = {
  token: () => localStorage.getItem(CLAVE_TOKEN),
  guardar: (token) => localStorage.setItem(CLAVE_TOKEN, token),
  cerrar: () => localStorage.removeItem(CLAVE_TOKEN),
};

export class ApiError extends Error {
  constructor(mensaje, status, detalles) {
    super(mensaje);
    this.status = status;
    this.detalles = detalles || {};
  }
}

async function peticion(ruta, { method = "GET", body, auth = true } = {}) {
  const headers = {};
  if (body !== undefined) headers["Content-Type"] = "application/json";
  const token = sesion.token();
  if (auth && token) headers.Authorization = `Bearer ${token}`;

  let respuesta;
  try {
    respuesta = await fetch(`${API_URL}${ruta}`, {
      method,
      headers,
      body: body !== undefined ? JSON.stringify(body) : undefined,
    });
  } catch {
    throw new ApiError("No hay conexión con el servidor. ¿Está encendido el backend?", 0);
  }

  if (respuesta.status === 204) return null;
  const datos = await respuesta.json().catch(() => null);

  if (!respuesta.ok) {
    if (respuesta.status === 401 && token) {
      sesion.cerrar();
      window.dispatchEvent(new Event("sesion-expirada"));
    }
    const error = datos?.error || {};
    throw new ApiError(error.mensaje || `Error HTTP ${respuesta.status}`, respuesta.status, error.detalles);
  }
  return datos;
}

const query = (params) => {
  const limpio = Object.fromEntries(
    Object.entries(params).filter(([, v]) => v !== undefined && v !== null && v !== "")
  );
  const texto = new URLSearchParams(limpio).toString();
  return texto ? `?${texto}` : "";
};

// ---- Sistema ----
export const getHealth = () => peticion("/health", { auth: false });

// ---- Autenticación ----
export const registrar = (datos) => peticion("/api/auth/register", { method: "POST", body: datos, auth: false });
export const login = (datos) => peticion("/api/auth/login", { method: "POST", body: datos, auth: false });
export const getPerfil = () => peticion("/api/auth/me");

// ---- Libros ----
export const getLibros = (filtros) => peticion(`/api/libros${query(filtros)}`, { auth: false });
export const getCategorias = () => peticion("/api/libros/categorias", { auth: false });
export const getLibro = (id) => peticion(`/api/libros/${id}`, { auth: false });
export const getContenido = (id) => peticion(`/api/libros/${id}/contenido`);
export const crearLibro = (datos) => peticion("/api/libros", { method: "POST", body: datos });
export const actualizarLibro = (id, datos) => peticion(`/api/libros/${id}`, { method: "PUT", body: datos });
export const eliminarLibro = (id) => peticion(`/api/libros/${id}`, { method: "DELETE" });

// ---- Reseñas ----
export const getResenas = (libroId, filtros = {}) =>
  peticion(`/api/libros/${libroId}/resenas${query(filtros)}`, { auth: false });
export const crearResena = (libroId, datos) =>
  peticion(`/api/libros/${libroId}/resenas`, { method: "POST", body: datos });
export const eliminarResena = (id) => peticion(`/api/resenas/${id}`, { method: "DELETE" });

// ---- Mi biblioteca ----
export const getMiBiblioteca = (filtros = {}) => peticion(`/api/mi-biblioteca${query(filtros)}`);
export const getLectura = (libroId) => peticion(`/api/mi-biblioteca/${libroId}`);
export const guardarLectura = (libroId, datos) =>
  peticion(`/api/mi-biblioteca/${libroId}`, { method: "PUT", body: datos });
export const quitarLectura = (libroId) => peticion(`/api/mi-biblioteca/${libroId}`, { method: "DELETE" });
