import { useEffect, useState } from "react";

import { listarMisLibros } from "../api";

function MisLibros({ alSeleccionar }) {
  const [progresos, setProgresos] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    listarMisLibros()
      .then((datos) => setProgresos(datos.progresos))
      .catch((problema) => setError(problema.message));
  }, []);

  if (error) {
    return <p className="error">{error}</p>;
  }

  if (progresos.length === 0) {
    return (
      <p>Todavia no ha registrado progreso en ningun libro del catalogo.</p>
    );
  }

  return (
    <div className="rejilla">
      {progresos.map((progreso) => (
        <article
          key={progreso.libro_id}
          className="libro"
          onClick={() => alSeleccionar(progreso.libro_id)}
        >
          <span className="etiqueta">{progreso.estado}</span>
          <h3>{progreso.titulo}</h3>
          <p className="meta">
            Pagina {progreso.pagina_actual} de {progreso.total_paginas}
          </p>
          <div className="barra">
            <div
              className="barra-avance"
              style={{ width: `${progreso.porcentaje}%` }}
            />
          </div>
          <p className="meta">{progreso.porcentaje}% leido</p>
        </article>
      ))}
    </div>
  );
}

export default MisLibros;
