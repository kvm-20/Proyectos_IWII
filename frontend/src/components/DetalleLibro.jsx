import { useEffect, useState } from "react";

import { actualizarProgreso, obtenerLibro, publicarResena } from "../api";

function DetalleLibro({ libroId, usuario, alVolver }) {
  const [libro, setLibro] = useState(null);
  const [error, setError] = useState(null);
  const [mensaje, setMensaje] = useState(null);

  const [calificacion, setCalificacion] = useState(5);
  const [comentario, setComentario] = useState("");
  const [pagina, setPagina] = useState(0);
  const [estado, setEstado] = useState("leyendo");

  function cargar() {
    obtenerLibro(libroId)
      .then((datos) => {
        setLibro(datos);
        setError(null);
      })
      .catch((problema) => setError(problema.message));
  }

  useEffect(cargar, [libroId]);

  async function enviarResena(evento) {
    evento.preventDefault();
    try {
      await publicarResena(libroId, { calificacion, comentario });
      setMensaje("Resena publicada.");
      setComentario("");
      cargar();
    } catch (problema) {
      setError(problema.message);
    }
  }

  async function guardarProgreso(evento) {
    evento.preventDefault();
    try {
      const resultado = await actualizarProgreso(libroId, {
        pagina_actual: pagina,
        estado,
      });
      setMensaje(`Progreso guardado: ${resultado.porcentaje}% leido.`);
    } catch (problema) {
      setError(problema.message);
    }
  }

  if (error) {
    return (
      <section className="tarjeta">
        <p className="error">{error}</p>
        <button onClick={alVolver}>Volver al catalogo</button>
      </section>
    );
  }

  if (!libro) {
    return <p>Cargando libro...</p>;
  }

  return (
    <section>
      <button className="boton-secundario" onClick={alVolver}>
        Volver al catalogo
      </button>

      <article className="tarjeta">
        <span className="etiqueta">{libro.categoria}</span>
        <h2>{libro.titulo}</h2>
        <p className="autor">{libro.autor}</p>
        <p className="meta">
          {libro.anio} - {libro.paginas} paginas - {libro.formato}
        </p>
        <p>{libro.descripcion}</p>
        <p className="calificacion">
          Calificacion promedio: {libro.calificacion_promedio} / 5 (
          {libro.total_resenas} resenas)
        </p>
      </article>

      {mensaje && <p className="exito">{mensaje}</p>}

      {usuario && (
        <div className="columnas">
          <section className="tarjeta">
            <h3>Mi progreso de lectura</h3>
            <form className="formulario" onSubmit={guardarProgreso}>
              <label>
                Pagina actual
                <input
                  type="number"
                  min="0"
                  max={libro.paginas}
                  value={pagina}
                  onChange={(evento) => setPagina(Number(evento.target.value))}
                />
              </label>

              <label>
                Estado
                <select
                  value={estado}
                  onChange={(evento) => setEstado(evento.target.value)}
                >
                  <option value="leyendo">Leyendo</option>
                  <option value="leido">Leido</option>
                  <option value="favorito">Favorito</option>
                </select>
              </label>

              <button type="submit">Guardar progreso</button>
            </form>
          </section>

          <section className="tarjeta">
            <h3>Escribir una resena</h3>
            <form className="formulario" onSubmit={enviarResena}>
              <label>
                Calificacion
                <select
                  value={calificacion}
                  onChange={(evento) =>
                    setCalificacion(Number(evento.target.value))
                  }
                >
                  {[5, 4, 3, 2, 1].map((valor) => (
                    <option key={valor} value={valor}>
                      {valor} / 5
                    </option>
                  ))}
                </select>
              </label>

              <label>
                Comentario
                <textarea
                  rows="3"
                  value={comentario}
                  onChange={(evento) => setComentario(evento.target.value)}
                />
              </label>

              <button type="submit">Publicar resena</button>
            </form>
          </section>
        </div>
      )}

      <section className="tarjeta">
        <h3>Resenas de los lectores</h3>
        {libro.resenas.length === 0 && <p>Este libro aun no tiene resenas.</p>}
        <ul className="lista-resenas">
          {libro.resenas.map((resena) => (
            <li key={resena.id}>
              <strong>{resena.usuario}</strong>
              <span className="calificacion"> {resena.calificacion} / 5</span>
              <p>{resena.comentario}</p>
            </li>
          ))}
        </ul>
      </section>
    </section>
  );
}

export default DetalleLibro;
