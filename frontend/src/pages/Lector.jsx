import { useEffect, useMemo, useRef, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { getContenido, getLectura, guardarLectura } from "../api";
import { Cargando, MensajeError } from "../components/Comunes";
import { usePeticion } from "../usePeticion";

// Visor de lectura: cada párrafo del contenido es una "página".
// El progreso se guarda automáticamente en el backend al cambiar de página.
export default function Lector() {
  const { id } = useParams();
  const { datos, cargando, error, recargar } = usePeticion(
    () => Promise.all([getContenido(id), getLectura(id)]),
    [id]
  );
  const [pagina, setPagina] = useState(0);
  const [guardado, setGuardado] = useState("");
  const listo = useRef(false);

  const [libro, lectura] = datos || [];
  const paginas = useMemo(
    () => (libro?.contenido || "").split(/\n\s*\n/).map((p) => p.trim()).filter(Boolean),
    [libro]
  );

  // Retoma la lectura donde el usuario la dejó.
  useEffect(() => {
    if (!libro) return;
    const ultima = lectura?.pagina_actual ? Math.min(lectura.pagina_actual, paginas.length) - 1 : 0;
    setPagina(Math.max(0, ultima));
    listo.current = true;
  }, [libro, lectura, paginas.length]);

  // Guarda el progreso cada vez que cambia la página.
  useEffect(() => {
    if (!listo.current || paginas.length === 0) return;
    setGuardado("Guardando...");
    guardarLectura(id, { pagina_actual: pagina + 1, total_paginas: paginas.length })
      .then(() => setGuardado("Progreso guardado ✓"))
      .catch(() => setGuardado("No se pudo guardar el progreso"));
  }, [pagina, id, paginas.length]);

  if (cargando) return <Cargando texto="Abriendo el libro..." />;
  if (error) return <MensajeError error={error} onReintentar={recargar} />;
  if (!libro) return null;

  const porcentaje = paginas.length ? Math.round(((pagina + 1) / paginas.length) * 100) : 0;

  return (
    <section className="lector">
      <Link to={`/libros/${id}`} className="volver">← Volver al libro</Link>
      <h1>{libro.titulo}</h1>
      <p className="subtitulo">{libro.autor}</p>

      <div className="progreso">
        <div className="progreso-barra" style={{ width: `${porcentaje}%` }} />
      </div>
      <small>{porcentaje}% leído · {guardado}</small>

      <div className="pagina-lectura">
        {paginas.length ? <p>{paginas[pagina]}</p> : <p>Este libro aún no tiene contenido.</p>}
      </div>

      <div className="paginacion">
        <button className="boton boton-secundario" disabled={pagina === 0} onClick={() => setPagina(pagina - 1)}>
          ← Anterior
        </button>
        <span>Página {pagina + 1} de {paginas.length || 1}</span>
        <button
          className="boton"
          disabled={pagina >= paginas.length - 1}
          onClick={() => setPagina(pagina + 1)}
        >
          Siguiente →
        </button>
      </div>
    </section>
  );
}
