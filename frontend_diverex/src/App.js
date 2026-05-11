import "./App.css";
import MapView from "./components/mapa/MapView";
import LoginModal from "./components/loginup/LoginModal";
import UserPanel from "./components/user/UserPanel";
import Alert from "./components/alerta/Alert";
import Filtros from "./components/filtros/Filtros";
import { AuthProvider, AuthContext } from "./context/AuthContext";
import { useContext, useState } from "react";
import LugarCard from "./components/lugar/LugarCard";
import ComentariosPanel from "./components/comentarios/ComentariosPanel"

function MainLayout() {
  const { user } = useContext(AuthContext);
  const [lugarId, setLugarId] = useState(null);
  const [showComment, setShowComment] = useState(false);
  const [userLocation, setUserLocation] = useState(null);
  const [filters, setFilters] = useState({
    sillaRuedas: false,
    zonaInfantil: false,
    comedor: false,
    distanciaMax: 50,
    tiposSeleccionados: [],
    estadosSeleccionados: ['B', 'R', 'M', 'E'] // <--- IMPORTANTE AÑADIR ESTO
  });

  //estado global de alertas
  const [alertData, setAlertData] = useState(null);


  return (
    <div className="App">
      <MapView setUserLocation={setUserLocation} filters={filters} userLocation={userLocation} />

      {/* ALERTA GLOBAL */}
      {alertData && (
        <Alert
          title={alertData.title}
          message={alertData.message}
          type={alertData.type}
          onClose={() => setAlertData(null)}
        />
      )}

      <div id="panelFlotante">
        {/* Login/Logup si no datos guardados */}
        {!user && <LoginModal setAlert={setAlertData} />}

        {/* Panel si hay usuario */}
        {user && <UserPanel setAlert={setAlertData} setLugarId={setLugarId} />}

        {/* Línea separadora opcional para que quede más limpio visualmente */}
        <hr style={{ width: "100%", border: "none", borderTop: "1px solid #e5e7eb", margin: "10px 0" }} />

        {/* COMPONENTE DE FILTROS MODULAR Y ESTÁTICO */}
        <Filtros
          filters={filters}
          setFilters={setFilters}
          userLocation={userLocation}
        />
      </div>

      <div id="panelFlotanteDos">
        {/* Panel si se busca un lugar */}
        {lugarId && <LugarCard lugarId={lugarId} setAlert={setAlertData} showComment={showComment} setShowComment={setShowComment} onClose={() => setLugarId(null)} />}

        {/* Panel muetra los comentarios */}
        {showComment && lugarId && <ComentariosPanel lugarId={lugarId} setAlert={setAlertData} />}
      </div>
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <MainLayout />
    </AuthProvider>
  );
}

export default App;