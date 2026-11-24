import { useEffect, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { getCategorias, getLibros } from "../api";
import { Cargando, Estrellas, MensajeError, Portada, Vacio } from "../components/Comunes";
import { usePeticion } from "../usePeticion";

const ORDENES = [
  { valor: "titulo:asc", texto: "Título (A-Z)" },
  { valor: "autor:asc", texto: "Autor (A-Z)" },
  { valor: "calificacion:desc", texto: "Mejor calificados" },
  { valor: "anio:desc", texto: "Más nuevos" },
  { valor: "anio:asc", texto: "Más antiguos" },
];

export default function Catalogo() {
  // Los filtros viven en la URL: ?q=...&categoria=...&page=2
  const [params, setParams] = useSearchParams();
  const q = params.get("q") || "";
  const categoria = params.get("categoria") || "";
  const orden = params.get("orden") || "titulo:asc";
  const page = Number(params.get("page") || 1);
  const [texto, setTexto] = useState(q);

  useEffect(() => setTexto(q), [q]);

  const [campo, direccion] = orden.split(":");
  const { datos, cargando, error, recargar } = usePeticion(
    () => getLibros({ q, categoria, orden: campo, direccion, page, limit: 8 }),
    [q, categoria, orden, page]
  );
  const categorias = usePeticion(getCategorias, []);

  const actualizar = (cambios) => {
    const nuevos = Object.fromEntries(params);
    Object.assign(nuevos, cambios);
    if (!("page" in cambios)) nuevos.page = 1;
    Object.keys(nuevos).forEach((k) => (nuevos[k] === "" || nuevos[k] === 1) && delete nuevos[k]);
    setParams(nuevos);
  };

  const buscar = (e) => {
    e.preventDefault();
    actualizar({ q: texto.trim() });
  };

  return (
    <section>
      <div className="encabezado">
        <h1>Catálogo de libros</h1>
        <p className="subtitulo">Biblioteca virtual interactiva de lectura en línea</p>
      </div>

      <form className="filtros" onSubmit={buscar}>
        <input
          type="search"
          placeholder="Buscar por título o autor..."
          value={texto}
          onChange={(e) => setTexto(e.target.value)}
          aria-label="Buscar"
        />
        <select value={categoria} onChange={(e) => actualizar({ categoria: e.target.value })} aria-label="Categoría">
          <option value="">Todas las categorías</option>
          {(categorias.datos || []).map((c) => (
            <option key={c} value={c}>{c}</option>
          ))}
        </select>
        <select value={orden} onChange={(e) => actualizar({ orden: e.target.value })} aria-label="Ordenar">
          {ORDENES.map((o) => (
            <option key={o.valor} value={o.valor}>{o.texto}</option>
          ))}
        </select>
        <button className="boton" type="submit">Buscar</button>
      </form>

      {cargando && <Cargando texto="Consultando el catálogo..." />}
      <MensajeError error={error} onReintentar={recargar} />

      {!cargando && !error && datos && (
        <>
          {datos.items.length === 0 ? (
            <Vacio>No encontramos libros con esos filtros.</Vacio>
          ) : (
            <div className="grilla">
              {datos.items.map((libro) => (
                <Link to={`/libros/${libro.id}`} key={libro.id} className="tarjeta-libro">
                  <Portada libro={libro} />
                  <div className="tarjeta-libro-info">
                    <h3>{libro.titulo}</h3>
                    <p>{libro.autor} · {libro.anio}</p>
                    <span className="etiqueta">{libro.categoria}</span>
                    <Estrellas valor={libro.calificacion_promedio} total={libro.total_resenas} />
                  </div>
                </Link>
              ))}
            </div>
          )}

          <div className="paginacion">
            <button
              className="boton boton-secundario"
              disabled={!datos.paginacion.tiene_anterior}
              onClick={() => actualizar({ page: page - 1 })}
            >
              ← Anterior
            </button>
            <span>
              Página {datos.paginacion.page} de {datos.paginacion.paginas || 1} · {datos.paginacion.total} libros
            </span>
            <button
              className="boton boton-secundario"
              disabled={!datos.paginacion.tiene_siguiente}
              onClick={() => actualizar({ page: page + 1 })}
            >
              Siguiente →
            </button>
          </div>
        </>
      )}
    </section>
  );
}
