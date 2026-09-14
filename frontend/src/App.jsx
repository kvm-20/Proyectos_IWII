import { useEffect, useState } from "react";
import { getHealth } from "./api";
import "./App.css";

function App() {
  const [estado, setEstado] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    getHealth()
      .then((datos) => setEstado(datos))
      .catch((err) => setError(err.message));
  }, []);

  return (
    <div className="contenedor">
      <h1>BiblioWeb</h1>
      <p className="subtitulo">
        Biblioteca virtual interactiva de lectura en linea
      </p>

      <section className="tarjeta">
        <h2>Estado del backend</h2>

        {error && <p className="error">Sin conexion: {error}</p>}
        {!error && !estado && <p>Consultando el servidor...</p>}

        {estado && (
          <ul className="lista-estado">
            <li><strong>Estado:</strong> {estado.status}</li>
            <li><strong>Servicio:</strong> {estado.service}</li>
            <li><strong>Version:</strong> {estado.version}</li>
          </ul>
        )}
      </section>
    </div>
  );
}

export default App;