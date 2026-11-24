import { useEffect, useState } from "react";
import { Link, NavLink, Navigate, Outlet, useLocation, useNavigate } from "react-router-dom";
import { getHealth } from "../api";
import { useAuth } from "../context/AuthContext";
import { Cargando } from "./Comunes";

export function Navbar() {
  const { usuario, esAdmin, cerrarSesion } = useAuth();
  const navegar = useNavigate();

  const salir = () => {
    cerrarSesion();
    navegar("/");
  };

  return (
    <header className="navbar">
      <Link to="/" className="marca">
        📚 BiblioWeb
      </Link>
      <nav>
        <NavLink to="/" end>Catálogo</NavLink>
        {usuario && <NavLink to="/mi-biblioteca">Mi biblioteca</NavLink>}
        {esAdmin && <NavLink to="/admin">Administración</NavLink>}
      </nav>
      <div className="navbar-usuario">
        {usuario ? (
          <>
            <span>
              Hola, <strong>{usuario.nombre}</strong>
              {esAdmin && <span className="etiqueta">admin</span>}
            </span>
            <button className="boton boton-secundario boton-pequeno" onClick={salir}>
              Salir
            </button>
          </>
        ) : (
          <>
            <Link to="/login" className="boton boton-pequeno">Iniciar sesión</Link>
            <Link to="/registro" className="boton boton-secundario boton-pequeno">Registrarse</Link>
          </>
        )}
      </div>
    </header>
  );
}

function EstadoBackend() {
  const [estado, setEstado] = useState(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    getHealth().then(setEstado).catch(() => setError(true));
  }, []);

  if (error) return <span className="punto punto-rojo">Backend sin conexión</span>;
  if (!estado) return <span>Verificando backend...</span>;
  return (
    <span className={`punto ${estado.database === "ok" ? "punto-verde" : "punto-rojo"}`}>
      API {estado.version} · base de datos: {estado.database}
    </span>
  );
}

export function Layout() {
  return (
    <>
      <Navbar />
      <main className="contenedor">
        <Outlet />
      </main>
      <footer className="pie">
        <span>BiblioWeb · Ingeniería Web II · Universidad Manuela Beltrán</span>
        <EstadoBackend />
      </footer>
    </>
  );
}

// Protege rutas que requieren sesión (y opcionalmente rol admin).
export function RutaPrivada({ children, soloAdmin = false }) {
  const { usuario, cargando, esAdmin } = useAuth();
  const ubicacion = useLocation();
  if (cargando) return <Cargando texto="Verificando sesión..." />;
  if (!usuario) return <Navigate to="/login" replace state={{ desde: ubicacion.pathname }} />;
  if (soloAdmin && !esAdmin) return <Navigate to="/" replace />;
  return children;
}
