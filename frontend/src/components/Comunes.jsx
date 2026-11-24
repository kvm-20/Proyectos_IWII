// Componentes pequeños reutilizables: estados de carga/error, estrellas y portada.

export function Cargando({ texto = "Cargando..." }) {
  return (
    <div className="estado estado-cargando" role="status">
      <span className="spinner" aria-hidden="true" /> {texto}
    </div>
  );
}

export function MensajeError({ error, onReintentar }) {
  if (!error) return null;
  return (
    <div className="estado estado-error" role="alert">
      <strong>Algo salió mal:</strong> {error.message || String(error)}
      {onReintentar && (
        <button className="boton boton-secundario boton-pequeno" onClick={onReintentar}>
          Reintentar
        </button>
      )}
    </div>
  );
}

export function Vacio({ children }) {
  return <div className="estado estado-vacio">{children}</div>;
}

export function Estrellas({ valor = 0, total }) {
  const llenas = Math.round(valor);
  return (
    <span className="estrellas" title={`${valor} de 5`}>
      {"★".repeat(llenas)}
      <span className="estrellas-vacias">{"★".repeat(5 - llenas)}</span>
      {total !== undefined && <small> {Number(valor).toFixed(1)} ({total})</small>}
    </span>
  );
}

export function SelectorEstrellas({ valor, onChange }) {
  return (
    <div className="selector-estrellas" role="radiogroup" aria-label="Calificación">
      {[1, 2, 3, 4, 5].map((n) => (
        <button
          type="button"
          key={n}
          role="radio"
          aria-checked={valor === n}
          className={n <= valor ? "activa" : ""}
          onClick={() => onChange(n)}
        >
          ★
        </button>
      ))}
    </div>
  );
}

const PALETA = ["#6b4423", "#2f5d50", "#7a3b4f", "#2f4a6b", "#8a6d1f", "#4f3b78", "#5b6b2f"];

export function Portada({ libro, grande = false }) {
  const color = PALETA[(libro.id || 0) % PALETA.length];
  return (
    <div className={`portada ${grande ? "portada-grande" : ""}`} style={{ backgroundColor: color }}>
      <span className="portada-titulo">{libro.titulo}</span>
      <span className="portada-autor">{libro.autor}</span>
    </div>
  );
}

export function campoError(error, campo) {
  return error?.detalles?.[campo] ? <span className="campo-error">{error.detalles[campo]}</span> : null;
}
