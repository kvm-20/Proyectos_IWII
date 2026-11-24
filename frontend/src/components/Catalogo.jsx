import { useEffect, useState } from "react";

import { listarCategorias, listarLibros } from "../api";

function Catalogo({ alSeleccionar }) {
  const [libros, setLibros] = useState([]);
  const [categorias, setCategorias] = useState([]);
  const [buscar, setBuscar] = useState("");
  const [categoria, setCategoria] = useState("");
  const [error, setError] = useState(null);
  const [cargando, setCargando] = useState(true);

  useEffect(() => {
    listarCategorias()
      .then((datos) => setCategorias(datos.categorias))
      .catch(() => setCategorias([]));
  }, []);

  useEffect(() => {
    setCargando(true);
    listarLibros({ buscar, categoria })
      .then((datos) => {
        setLibros(datos.libros);
        setError(null);
      })
      .catch((problema) => setError(problema.message))
      .finally(() => setCargando(false));
  }, [buscar, categoria]);

  return (
    <section>
      <div className="filtros">
        <input
          type="search"
          placeholder="Buscar por titulo o autor"
          value={buscar}
          onChange={(evento) => setBuscar(evento.target.value)}
        />

        <select
          value={categoria}
          onChange={(evento) => setCategoria(evento.target.value)}
        >
          <option value="">Todas las categorias</option>
          {categorias.map((nombre) => (
            <option key={nombre} value={nombre}>
              {nombre}
            </option>
          ))}
        </select>
      </div>

      {error && <p className="error">{error}</p>}
      {cargando && <p>Cargando catalogo...</p>}
      {!cargando && libros.length === 0 && <p>No se encontraron libros.</p>}

      <div className="rejilla">
        {libros.map((libro) => (
          <article
            key={libro.id}
            className="libro"
            onClick={() => alSeleccionar(libro.id)}
          >
            <span className="etiqueta">{libro.categoria}</span>
            <h3>{libro.titulo}</h3>
            <p className="autor">{libro.autor}</p>
            <p className="meta">
              {libro.anio} - {libro.paginas} paginas - {libro.formato}
            </p>
            <p className="calificacion">
              {libro.calificacion_promedio > 0
                ? `${libro.calificacion_promedio} / 5 (${libro.total_resenas})`
                : "Sin calificaciones"}
            </p>
          </article>
        ))}
      </div>
    </section>
  );
}

export default Catalogo;
