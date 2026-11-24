import { useState } from "react";
import { Link } from "react-router-dom";
import { getMiBiblioteca } from "../api";
import { Cargando, MensajeError, Vacio } from "../components/Comunes";
import { usePeticion } from "../usePeticion";

const PESTANAS = [
  { id: "todos", texto: "Todos", filtro: {} },
  { id: "favoritos", texto: "♥ Favoritos", filtro: { favorito: "true" } },
  { id: "leyendo", texto: "Leyendo", filtro: { estado: "leyendo" } },
  { id: "leido", texto: "Leídos", filtro: { estado: "leido" } },
  { id: "pendiente", texto: "Pendientes", filtro: { estado: "pendiente" } },
];

const ETIQUETA_ESTADO = { pendiente: "Pendiente", leyendo: "Leyendo", leido: "Leído" };

export default function MiBiblioteca() {
  const [pestana, setPestana] = useState(PESTANAS[0]);
  const { datos, cargando, error, recargar } = usePeticion(
    () => getMiBiblioteca(pestana.filtro),
    [pestana.id]
  );

  return (
    <section>
      <div className="encabezado">
        <h1>Mi biblioteca</h1>
        <p className="subtitulo">Tus listas personales y tu progreso de lectura</p>
      </div>

      <div className="pestanas" role="tablist">
        {PESTANAS.map((p) => (
          <button
            key={p.id}
            role="tab"
            aria-selected={p.id === pestana.id}
            className={p.id === pestana.id ? "activa" : ""}
            onClick={() => setPestana(p)}
          >
            {p.texto}
          </button>
        ))}
      </div>

      {cargando && <Cargando />}
      <MensajeError error={error} onReintentar={recargar} />
      {datos && datos.length === 0 && (
        <Vacio>
          No hay libros en esta lista. <Link to="/">Explora el catálogo</Link>.
        </Vacio>
      )}

      <ul className="lista-lecturas">
        {datos?.map((l) => (
          <li key={l.libro.id} className="tarjeta">
            <div className="fila fila-espaciada">
              <div>
                <Link to={`/libros/${l.libro.id}`}><strong>{l.libro.titulo}</strong></Link>
                <p className="subtitulo">{l.libro.autor}</p>
              </div>
              <div className="fila">
                {l.favorito && <span title="Favorito">♥</span>}
                <span className="etiqueta">{ETIQUETA_ESTADO[l.estado]}</span>
              </div>
            </div>
            <div className="progreso">
              <div className="progreso-barra" style={{ width: `${l.porcentaje}%` }} />
            </div>
            <div className="fila fila-espaciada">
              <small>{l.porcentaje}% leído</small>
              <Link to={`/libros/${l.libro.id}/leer`} className="boton boton-pequeno">
                {l.porcentaje > 0 ? "Continuar leyendo" : "Empezar a leer"}
              </Link>
            </div>
          </li>
        ))}
      </ul>
    </section>
  );
}
