import "./App.css";
import MapView from "./components/mapa/MapView";
import LoginModal from "./components/loginup/LoginModal";
import UserPanel from "./components/user/UserPanel";
import Alert from "./components/alerta/Alert";
import Loading from "./components/carga/Loading";
import Filtros from "./components/filtros/Filtros";
import { AuthProvider, AuthContext } from "./context/AuthContext";
import { useContext, useState } from "react";
import LugarCard from "./components/lugar/LugarCard";
import ComentariosPanel from "./components/comentarios/ComentariosPanel";
import List from "./components/lista/List";
import TopButton from "./components/top/TopButton";

function MainLayout() {
  const { user } = useContext(AuthContext);
  const [lugarId, setLugarId] = useState(null);
  const [showComment, setShowComment] = useState(false);
  const [userLocation, setUserLocation] = useState(null);

  // NUEVO: Estado para guardar la lista de lugares filtrados
  const [lugaresFiltrados, setLugaresFiltrados] = useState([]);

  const [filters, setFilters] = useState({
    sillaRuedas: false,
    zonaInfantil: false,
    comedor: false,
    distanciaMax: 50,
    tiposSeleccionados: [],
    estadosSeleccionados: ['B', 'R', 'M', 'E'],
    busquedaTexto: ""
  });

  const [modoFiltro, setModoFiltro] = useState(true);
  const [recommendationFilters, setRecommendationFilters] = useState({
      tipo: [],
      estado: [],
      accesible: null,
      //codigo_municipio: "",
      tipo_detalle: [],
      media_min: 1,
      media_max: 5,
      //caracteristicas parque
      agua: null,
      electricidad: null,
      comedor: null,
      juegos: null
  });

  const [modoTop, setModoTop] = useState(false);
  const [topFilters, setTopFilters] = useState({
      codigo_municipio: null,
      tipo_detalle: []
  });

  const [inputValue, setInputValue] = useState("");
  const ejecutarBusqueda = () => {
    setFilters({ ...filters, busquedaTexto: inputValue });
  };

  const [alertData, setAlertData] = useState(null);
  const [loading, setLoading] = useState({ visible: false, text: "Cargando..." });

  return (
    <div className="App">
      {/* Añadimos setLugaresFiltrados como prop al MapView */}
      <MapView 
        setUserLocation={setUserLocation} 
        filters={filters} 
        modoFiltro={modoFiltro} 
        recommendationFilters={recommendationFilters}
        userLocation={userLocation} 
        setLugarId={setLugarId} 
        setLugaresFiltrados={setLugaresFiltrados}
        lugaresFiltrados={lugaresFiltrados}
        lugarId={lugarId}
        setLoading={setLoading}
        modoTop={modoTop}
        topFilters={topFilters}
      />

      {alertData && (
        <Alert
          title={alertData.title}
          message={alertData.message}
          type={alertData.type}
          onClose={() => setAlertData(null)}
        />
      )}

      {/* --- BARRA DE BÚSQUEDA CON BOTÓN --- */}
      <div className="buscador-superior">
        <div className="buscador-input-wrapper">
          <span className="icono-lupa">🔍</span>
          <input
            type="text"
            placeholder="Ej: Parque, Badajoz"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter') ejecutarBusqueda();
            }}
          />
          <button className="btn-buscar-texto" onClick={ejecutarBusqueda}>
            Buscar
          </button>
        </div>
      </div>

      <div id="panelFlotante">
        {!user && <LoginModal setAlert={setAlertData} />}
        {user && <UserPanel setAlert={setAlertData} setLugarId={setLugarId} />}

        <hr style={{ width: "100%", border: "none", borderTop: "1px solid #e5e7eb", margin: "10px 0" }} />

        {/* COMPONENTE DE FILTROS MODULAR Y ESTÁTICO */}
        <Filtros
          filters={filters}
          setFilters={setFilters}
          userLocation={userLocation}
          modoFiltro={modoFiltro}
          setModoFiltro={setModoFiltro}
          recommendationFilters={recommendationFilters}
          setRecommendationFilters={setRecommendationFilters}
        />
      </div>
      
      <TopButton
        modoTop={modoTop}
        setModoTop={setModoTop}
        topFilters={topFilters}
        setTopFilters={setTopFilters}
      />

      <div id="panelFlotanteDos">
        {(lugarId || lugaresFiltrados.length > 0) && (
          <div className="columna-blanca-unica">

            {/* DETALLE DEL LUGAR */}
            {lugarId && (
              <LugarCard
                lugarId={lugarId}
                setAlert={setAlertData}
                showComment={showComment}
                setShowComment={setShowComment}
                onClose={() => setLugarId(null)}
              />
            )}

            {/* COMENTARIOS */}
            {showComment && lugarId && (
              <ComentariosPanel lugarId={lugarId} setAlert={setAlertData} />
            )}

            {/* LISTA DE RESULTADOS */}
            {lugaresFiltrados.length > 0 && (
              <div className="seccion-resultados-lista">
                <h3 className="titulo-resultados">
                  Resultados ({lugaresFiltrados.length})
                </h3>
                <List items={lugaresFiltrados} setLugarId={setLugarId} />
              </div>
            )}

          </div>
        )}

        <Loading visible={loading.visible}  text={loading.text} />
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