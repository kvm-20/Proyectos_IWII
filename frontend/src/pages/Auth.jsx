import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { registrar } from "../api";
import { campoError, MensajeError } from "../components/Comunes";
import { useAuth } from "../context/AuthContext";

export function Login() {
  const { iniciarSesion } = useAuth();
  const navegar = useNavigate();
  const ubicacion = useLocation();
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState(null);
  const [enviando, setEnviando] = useState(false);
  const registrado = ubicacion.state?.registrado;

  const enviar = async (e) => {
    e.preventDefault();
    setEnviando(true);
    setError(null);
    try {
      await iniciarSesion(form.email, form.password);
      navegar(ubicacion.state?.desde || "/", { replace: true });
    } catch (err) {
      setError(err);
    } finally {
      setEnviando(false);
    }
  };

  return (
    <section className="tarjeta formulario">
      <h1>Iniciar sesión</h1>
      {registrado && <div className="estado estado-ok">Cuenta creada. Ya puedes iniciar sesión.</div>}
      <form onSubmit={enviar}>
        <label>
          Correo
          <input type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} required />
          {campoError(error, "email")}
        </label>
        <label>
          Contraseña
          <input type="password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} required />
          {campoError(error, "password")}
        </label>
        {error && !error.detalles?.email && <MensajeError error={error} />}
        <button className="boton" disabled={enviando}>{enviando ? "Ingresando..." : "Ingresar"}</button>
      </form>
      <p>¿No tienes cuenta? <Link to="/registro">Regístrate</Link></p>
      <p className="ayuda">Cuentas de prueba: lector@biblioweb.com / Lector123* · admin@biblioweb.com / Admin123*</p>
    </section>
  );
}

export function Registro() {
  const navegar = useNavigate();
  const [form, setForm] = useState({ nombre: "", email: "", password: "" });
  const [error, setError] = useState(null);
  const [enviando, setEnviando] = useState(false);

  const enviar = async (e) => {
    e.preventDefault();
    setEnviando(true);
    setError(null);
    try {
      await registrar(form);
      navegar("/login", { state: { registrado: true } });
    } catch (err) {
      setError(err);
    } finally {
      setEnviando(false);
    }
  };

  const cambiar = (campo) => (e) => setForm({ ...form, [campo]: e.target.value });

  return (
    <section className="tarjeta formulario">
      <h1>Crear cuenta</h1>
      <form onSubmit={enviar} noValidate>
        <label>
          Nombre
          <input value={form.nombre} onChange={cambiar("nombre")} />
          {campoError(error, "nombre")}
        </label>
        <label>
          Correo
          <input type="email" value={form.email} onChange={cambiar("email")} />
          {campoError(error, "email")}
        </label>
        <label>
          Contraseña (mínimo 6 caracteres)
          <input type="password" value={form.password} onChange={cambiar("password")} />
          {campoError(error, "password")}
        </label>
        {error && error.status !== 422 && <MensajeError error={error} />}
        <button className="boton" disabled={enviando}>{enviando ? "Creando..." : "Registrarme"}</button>
      </form>
      <p>¿Ya tienes cuenta? <Link to="/login">Inicia sesión</Link></p>
    </section>
  );
}
