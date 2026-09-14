const API_URL = import.meta.env.VITE_API_URL;

export async function getHealth() {
  const respuesta = await fetch(`${API_URL}/health`);

  if (!respuesta.ok) {
    throw new Error(`Error HTTP ${respuesta.status}`);
  }

  return respuesta.json();
}