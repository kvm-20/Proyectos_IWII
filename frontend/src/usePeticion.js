import { useCallback, useEffect, useState } from "react";

// Hook que maneja los 3 estados al consumir la API: loading, error y data.
export function usePeticion(funcion, dependencias = []) {
  const [datos, setDatos] = useState(null);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState(null);
  const [version, setVersion] = useState(0);

  useEffect(() => {
    let activo = true; // cleanup: evita actualizar el estado si el componente ya se desmontó
    setCargando(true);
    setError(null);
    funcion()
      .then((respuesta) => activo && setDatos(respuesta))
      .catch((err) => activo && setError(err))
      .finally(() => activo && setCargando(false));
    return () => {
      activo = false;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [...dependencias, version]);

  const recargar = useCallback(() => setVersion((v) => v + 1), []);
  return { datos, cargando, error, recargar, setDatos };
}
