import "./App.css";
import MapView from "./components/MapView";
import LoginModal from "./components/loginup/LoginModal";
import UserPanel from "./components/user/UserPanel";
import Alert from "./components/alerta/Alert";
import { AuthProvider, AuthContext } from "./context/AuthContext";
import { useContext, useState } from "react";
import LugarCard from "./components/lugar/LugarCard";
import ComentariosPanel from "./components/comentarios/ComentariosPanel"

function MainLayout() {
  const { user } = useContext(AuthContext);
  const [lugarId, setLugarId] = useState(null);
  const [showComment, setShowComment] = useState(false);

  //estado global de alertas
  const [alertData, setAlertData] = useState(null);

  return (
    <div className="App">
      {/* Mapa SIEMPRE visible */}
      {console.log("API URL:", process.env.REACT_APP_API_URL)}
      <MapView />

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
      </div>

      <div id="panelFlotanteDos">
        {/* Panel si se busca un lugar */}
        {lugarId && <LugarCard lugarId={lugarId} setAlert={setAlertData} showComment={showComment} setShowComment={setShowComment} onClose={() => setLugarId(null)} />}

        {/* Panel muetra los comentarios */}
        {showComment && <ComentariosPanel lugarId={lugarId} setAlert={setAlertData} />}
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