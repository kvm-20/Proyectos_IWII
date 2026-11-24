import { useState } from "react";
import { actualizarLibro, crearLibro, eliminarLibro, getContenido, getLibros } from "../api";
import { Cargando, campoError, MensajeError } from "../components/Comunes";
import { usePeticion } from "../usePeticion";

const VACIO = {
  titulo: "",
  autor: "",
  categoria: "",
  anio: "",
  idioma: "Español",
  descripcion: "",
  contenido: "",
  url_externa: "",
};

function FormularioLibro({ inicial, onGuardado, onCancelar }) {
  const [form, setForm] = useState(inicial || VACIO);
  const [error, setError] = useState(null);
  const [enviando, setEnviando] = useState(false);
  const editando = Boolean(inicial?.id);

  const cambiar = (campo) => (e) => setForm({ ...form, [campo]: e.target.value });

  const enviar = async (e) => {
    e.preventDefault();
    setEnviando(true);
    setError(null);
    const datos = { ...form, anio: form.anio === "" ? null : Number(form.anio) };
    delete datos.id;
    try {
      if (editando) await actualizarLibro(inicial.id, datos);
      else await crearLibro(datos);
      onGuardado();
    } catch (err) {
      setError(err);
    } finally {
      setEnviando(false);
    }
  };

  return (
    <form className="tarjeta formulario-admin" onSubmit={enviar} noValidate>
      <h2>{editando ? `Editar: ${inicial.titulo}` : "Agregar libro"}</h2>
      <div className="columnas">
        <label>Título *<input value={form.titulo} onChange={cambiar("titulo")} />{campoError(error, "titulo")}</label>
        <label>Autor *<input value={form.autor} onChange={cambiar("autor")} />{campoError(error, "autor")}</label>
        <label>Categoría *<input value={form.categoria} onChange={cambiar("categoria")} />{campoError(error, "categoria")}</label>
        <label>Año<input type="number" value={form.anio ?? ""} onChange={cambiar("anio")} />{campoError(error, "anio")}</label>
        <label>Idioma<input value={form.idioma || ""} onChange={cambiar("idioma")} /></label>
        <label>URL obra completa<input value={form.url_externa || ""} onChange={cambiar("url_externa")} />{campoError(error, "url_externa")}</label>
      </div>
      <label>Descripción<textarea value={form.descripcion || ""} onChange={cambiar("descripcion")} /></label>
      <label>
        Contenido (separe las páginas con una línea en blanco)
        <textarea rows={6} value={form.contenido || ""} onChange={cambiar("contenido")} />
      </label>
      {error && error.status !== 422 && <MensajeError error={error} />}
      <div className="fila">
        <button className="boton" disabled={enviando}>{enviando ? "Guardando..." : "Guardar"}</button>
        <button type="button" className="boton boton-secundario" onClick={onCancelar}>Cancelar</button>
      </div>
    </form>
  );
}

export default function Admin() {
  const [page, setPage] = useState(1);
  const { datos, cargando, error, recargar } = usePeticion(
    () => getLibros({ page, limit: 10, orden: "recientes", direccion: "desc" }),
    [page]
  );
  const [editando, setEditando] = useState(null); // null = cerrado, {} = nuevo, libro = editar
  const [mensaje, setMensaje] = useState("");
  const [errorAccion, setErrorAccion] = useState(null);

  const abrirEdicion = async (libro) => {
    // Se trae el contenido completo (requiere token) para poder editarlo.
    const completo = await getContenido(libro.id);
    setEditando(completo);
  };

  const borrar = async (libro) => {
    if (!window.confirm(`¿Eliminar "${libro.titulo}"? Esta acción no se puede deshacer.`)) return;
    setErrorAccion(null);
    try {
      await eliminarLibro(libro.id);
      setMensaje(`"${libro.titulo}" fue eliminado.`);
      recargar();
    } catch (err) {
      setErrorAccion(err);
    }
  };

  const guardado = () => {
    setMensaje(editando?.id ? "Libro actualizado." : "Libro creado.");
    setEditando(null);
    recargar();
  };

  return (
    <section>
      <div className="encabezado fila fila-espaciada">
        <div>
          <h1>Administración del catálogo</h1>
          <p className="subtitulo">Solo visible para el rol administrador</p>
        </div>
        {!editando && <button className="boton" onClick={() => setEditando({})}>+ Nuevo libro</button>}
      </div>

      {mensaje && <div className="estado estado-ok">{mensaje}</div>}
      <MensajeError error={errorAccion} />
      {editando && (
        <FormularioLibro
          key={editando.id || "nuevo"}
          inicial={editando.id ? editando : null}
          onGuardado={guardado}
          onCancelar={() => setEditando(null)}
        />
      )}

      {cargando && <Cargando />}
      <MensajeError error={error} onReintentar={recargar} />
      {datos && (
        <>
          <table className="tabla">
            <thead>
              <tr><th>Título</th><th>Autor</th><th>Categoría</th><th>Año</th><th>Reseñas</th><th></th></tr>
            </thead>
            <tbody>
              {datos.items.map((libro) => (
                <tr key={libro.id}>
                  <td>{libro.titulo}</td>
                  <td>{libro.autor}</td>
                  <td>{libro.categoria}</td>
                  <td>{libro.anio}</td>
                  <td>{libro.total_resenas}</td>
                  <td>
                    <div className="acciones">
                    <button className="boton boton-secundario boton-pequeno" onClick={() => abrirEdicion(libro)}>Editar</button>
                    <button className="boton boton-peligro boton-pequeno" onClick={() => borrar(libro)}>Eliminar</button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          <div className="paginacion">
            <button className="boton boton-secundario" disabled={!datos.paginacion.tiene_anterior} onClick={() => setPage(page - 1)}>← Anterior</button>
            <span>Página {page} de {datos.paginacion.paginas || 1}</span>
            <button className="boton boton-secundario" disabled={!datos.paginacion.tiene_siguiente} onClick={() => setPage(page + 1)}>Siguiente →</button>
          </div>
        </>
      )}
    </section>
  );
}
