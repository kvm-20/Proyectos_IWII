import { createContext, useCallback, useContext, useEffect, useState } from "react";
import { getPerfil, login as loginApi, sesion } from "../api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [usuario, setUsuario] = useState(null);
  const [cargando, setCargando] = useState(Boolean(sesion.token()));

  // Al abrir la app, si hay token guardado se recupera el usuario.
  useEffect(() => {
    if (!sesion.token()) return;
    getPerfil()
      .then(setUsuario)
      .catch(() => sesion.cerrar())
      .finally(() => setCargando(false));
  }, []);

  useEffect(() => {
    const expirar = () => setUsuario(null);
    window.addEventListener("sesion-expirada", expirar);
    return () => window.removeEventListener("sesion-expirada", expirar);
  }, []);

  const iniciarSesion = useCallback(async (email, password) => {
    const datos = await loginApi({ email, password });
    sesion.guardar(datos.access_token);
    setUsuario(datos.usuario);
    return datos.usuario;
  }, []);

  const cerrarSesion = useCallback(() => {
    sesion.cerrar();
    setUsuario(null);
  }, []);

  return (
    <AuthContext.Provider
      value={{ usuario, cargando, esAdmin: usuario?.rol === "admin", iniciarSesion, cerrarSesion }}
    >
      {children}
    </AuthContext.Provider>
  );
}

// eslint-disable-next-line react-refresh/only-export-components
export const useAuth = () => useContext(AuthContext);
