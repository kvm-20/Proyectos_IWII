import { useState } from "react";

import { guardarToken, iniciarSesion, registrar } from "../api";

function Login({ alIniciarSesion }) {
  const [modoRegistro, setModoRegistro] = useState(false);
  const [nombre, setNombre] = useState("");
  const [correo, setCorreo] = useState("");
  const [contrasena, setContrasena] = useState("");
  const [error, setError] = useState(null);
  const [cargando, setCargando] = useState(false);

  async function enviar(evento) {
    evento.preventDefault();
    setError(null);
    setCargando(true);

    try {
      const respuesta = modoRegistro
        ? await registrar({ nombre, correo, contrasena })
        : await iniciarSesion({ correo, contrasena });

      guardarToken(respuesta.token);
      alIniciarSesion(respuesta.usuario);
    } catch (problema) {
      setError(problema.message);
    } finally {
      setCargando(false);
    }
  }

  return (
    <section className="tarjeta">
      <h2>{modoRegistro ? "Crear cuenta" : "Iniciar sesion"}</h2>

      <form className="formulario" onSubmit={enviar}>
        {modoRegistro && (
          <label>
            Nombre
            <input
              type="text"
              value={nombre}
              onChange={(evento) => setNombre(evento.target.value)}
              required
            />
          </label>
        )}

        <label>
          Correo
          <input
            type="email"
            value={correo}
            onChange={(evento) => setCorreo(evento.target.value)}
            required
          />
        </label>

        <label>
          Contrasena
          <input
            type="password"
            value={contrasena}
            onChange={(evento) => setContrasena(evento.target.value)}
            minLength={8}
            required
          />
        </label>

        {error && <p className="error">{error}</p>}

        <button type="submit" disabled={cargando}>
          {cargando ? "Enviando..." : modoRegistro ? "Registrarme" : "Entrar"}
        </button>
      </form>

      <p className="cambio-modo">
        {modoRegistro ? "Ya tiene cuenta?" : "Aun no tiene cuenta?"}{" "}
        <button
          className="enlace"
          onClick={() => {
            setModoRegistro(!modoRegistro);
            setError(null);
          }}
        >
          {modoRegistro ? "Iniciar sesion" : "Registrarse"}
        </button>
      </p>
    </section>
  );
}

export default Login;
