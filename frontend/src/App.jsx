import { Route, Routes } from "react-router-dom";
import { Layout, RutaPrivada } from "./components/Layout";
import { Vacio } from "./components/Comunes";
import Admin from "./pages/Admin";
import { Login, Registro } from "./pages/Auth";
import Catalogo from "./pages/Catalogo";
import Lector from "./pages/Lector";
import LibroDetalle from "./pages/LibroDetalle";
import MiBiblioteca from "./pages/MiBiblioteca";
import "./App.css";

function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<Catalogo />} />
        <Route path="/login" element={<Login />} />
        <Route path="/registro" element={<Registro />} />
        <Route path="/libros/:id" element={<LibroDetalle />} />
        <Route path="/libros/:id/leer" element={<RutaPrivada><Lector /></RutaPrivada>} />
        <Route path="/mi-biblioteca" element={<RutaPrivada><MiBiblioteca /></RutaPrivada>} />
        <Route path="/admin" element={<RutaPrivada soloAdmin><Admin /></RutaPrivada>} />
        <Route path="*" element={<Vacio>Página no encontrada.</Vacio>} />
      </Route>
    </Routes>
  );
}

export default App;
