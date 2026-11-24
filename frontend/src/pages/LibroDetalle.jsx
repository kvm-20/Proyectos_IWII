import { useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import {
  crearResena,
  eliminarResena,
  getLectura,
  getLibro,
  getResenas,
  guardarLectura,
  quitarLectura,
} from "../api";
import {
  Cargando,
  campoError,
  Estrellas,
  MensajeError,
  Portada,
  SelectorEstrellas,
  Vacio,
} from "../components/Comunes";
import { useAuth } from "../context/AuthContext";
import { usePeticion } from "../usePeticion";

const ETIQUETA_ESTADO = { pendiente: "Pendiente", leyendo: "Leyendo", leido: "Leído" };

function PanelLectura({ libroId }) {
  const { datos: lectura, cargando, error, setDatos } = usePeticion(() => getLectura(libroId), [libroId]);
  const [errorAccion, setErrorAccion] = useState(null);

  const guardar = async (cambios) => {
    setErrorAccion(null);
    try {
      setDatos(await guardarLectura(libroId, cambios));
    } catch (err) {
      setErrorAccion(err);
    }
  };

  const quitar = async () => {
    await quitarLectura(libroId);
    setDatos(null);
  };

  if (cargando) return <Cargando texto="Consultando tu biblioteca..." />;
  if (error) return <MensajeError error={error} />;

  return (
    <div className="panel">
      <h3>Mi biblioteca</h3>
      <MensajeError error={errorAccion} />
      {!lectura ? (
        <button className="boton" onClick={() => guardar({ estado: "pendiente" })}>
          + Agregar a mi biblioteca
        </button>
      ) : (
        <>
          <div className="fila">
            <label>
              Estado:{" "}
              <select value={lectura.estado} onChange={(e) => guardar({ estado: e.target.value })}>
                {Object.entries(ETIQUETA_ESTADO).map(([valor, texto]) => (
                  <option key={valor} value={valor}>{texto}</option>
                ))}
              </select>
            </label>
            <button
              className={`boton boton-pequeno ${lectura.favorito ? "" : "boton-secundario"}`}
              onClick={() => guardar({ favorito: !lectura.favorito })}
            >
              {lectura.favorito ? "♥ Favorito" : "♡ Marcar favorito"}
            </button>
          </div>
          <div className="progreso" aria-label={`Progreso ${lectura.porcentaje}%`}>
            <div className="progreso-barra" style={{ width: `${lectura.porcentaje}%` }} />
          </div>
          <small>
            Progreso: {lectura.porcentaje}% (página {lectura.pagina_actual} de {lectura.total_paginas})
          </small>
          <div>
            <button className="enlace" onClick={quitar}>Quitar de mi biblioteca</button>
          </div>
        </>
      )}
    </div>
  );
}

function Resenas({ libroId, onCambio }) {
  const { usuario, esAdmin } = useAuth();
  const [minimo, setMinimo] = useState("");
  const [orden, setOrden] = useState("recientes");
  const { datos, cargando, error, recargar } = usePeticion(
    () => getResenas(libroId, { min: minimo, orden, limit: 20 }),
    [libroId, minimo, orden]
  );
  const [calificacion, setCalificacion] = useState(0);
  const [comentario, setComentario] = useState("");
  const [enviando, setEnviando] = useState(false);
  const [errorForm, setErrorForm] = useState(null);

  const yaReseno = datos?.items.some((r) => r.usuario.id === usuario?.id);

  const publicar = async (e) => {
    e.preventDefault();
    setEnviando(true);
    setErrorForm(null);
    try {
      await crearResena(libroId, { calificacion, comentario });
      setCalificacion(0);
      setComentario("");
      recargar();
      onCambio();
    } catch (err) {
      setErrorForm(err);
    } finally {
      setEnviando(false);
    }
  };

  const borrar = async (id) => {
    await eliminarResena(id);
    recargar();
    onCambio();
  };

  return (
    <section className="panel">
      <div className="fila fila-espaciada">
        <h2>Reseñas</h2>
        <div className="fila">
          <select value={minimo} onChange={(e) => setMinimo(e.target.value)} aria-label="Calificación mínima">
            <option value="">Todas las calificaciones</option>
            <option value="4">4 estrellas o más</option>
            <option value="5">Solo 5 estrellas</option>
          </select>
          <select value={orden} onChange={(e) => setOrden(e.target.value)} aria-label="Ordenar reseñas">
            <option value="recientes">Más recientes</option>
            <option value="calificacion">Mejor calificación</option>
          </select>
        </div>
      </div>

      {usuario && !yaReseno && (
        <form className="formulario-resena" onSubmit={publicar}>
          <SelectorEstrellas valor={calificacion} onChange={setCalificacion} />
          {campoError(errorForm, "calificacion")}
          <textarea
            placeholder="¿Qué te pareció el libro?"
            value={comentario}
            maxLength={1000}
            onChange={(e) => setComentario(e.target.value)}
          />
          {errorForm && !errorForm.detalles?.calificacion && <MensajeError error={errorForm} />}
          <button className="boton" disabled={enviando || calificacion === 0}>
            {enviando ? "Publicando..." : "Publicar reseña"}
          </button>
        </form>
      )}
      {!usuario && (
        <p>
          <Link to="/login">Inicia sesión</Link> para calificar y reseñar este libro.
        </p>
      )}

      {cargando && <Cargando texto="Cargando reseñas..." />}
      <MensajeError error={error} onReintentar={recargar} />
      {datos && datos.items.length === 0 && <Vacio>Aún no hay reseñas con ese filtro.</Vacio>}
      <ul className="lista-resenas">
        {datos?.items.map((r) => (
          <li key={r.id}>
            <div className="fila fila-espaciada">
              <strong>{r.usuario.nombre}</strong>
              <Estrellas valor={r.calificacion} />
            </div>
            {r.comentario && <p>{r.comentario}</p>}
            <small>{new Date(r.creado_en).toLocaleDateString("es-CO")}</small>
            {(r.usuario.id === usuario?.id || esAdmin) && (
              <button className="enlace" onClick={() => borrar(r.id)}>Eliminar</button>
            )}
          </li>
        ))}
      </ul>
    </section>
  );
}

export default function LibroDetalle() {
  const { id } = useParams();
  const { usuario } = useAuth();
  const navegar = useNavigate();
  const { datos: libro, cargando, error, recargar } = usePeticion(() => getLibro(id), [id]);

  if (cargando && !libro) return <Cargando texto="Cargando libro..." />;
  if (error) return <MensajeError error={error} onReintentar={recargar} />;
  if (!libro) return null;

  return (
    <article>
      <Link to="/" className="volver">← Volver al catálogo</Link>
      <div className="detalle">
        <Portada libro={libro} grande />
        <div className="detalle-info">
          <h1>{libro.titulo}</h1>
          <p className="subtitulo">{libro.autor} · {libro.anio} · {libro.idioma}</p>
          <span className="etiqueta">{libro.categoria}</span>
          <div><Estrellas valor={libro.calificacion_promedio} total={libro.total_resenas} /></div>
          <p>{libro.descripcion}</p>
          <div className="fila">
            <button
              className="boton"
              onClick={() => navegar(usuario ? `/libros/${libro.id}/leer` : "/login", { state: { desde: `/libros/${libro.id}/leer` } })}
            >
              📖 Leer ahora
            </button>
            {libro.url_externa && (
              <a className="boton boton-secundario" href={libro.url_externa} target="_blank" rel="noreferrer">
                Obra completa ↗
              </a>
            )}
          </div>
          {usuario && <PanelLectura libroId={libro.id} />}
        </div>
      </div>
      <Resenas libroId={libro.id} onCambio={recargar} />
    </article>
  );
}
