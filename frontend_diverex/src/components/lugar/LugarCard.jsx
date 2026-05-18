import { useEffect, useState, useContext } from "react";
import "./LugarCard.css";

import { AuthContext } from "../../context/AuthContext";

import { getPlace } from "../../apiServices/placesInfo";
import { getLikes, like, unlike } from "../../apiServices/likes";
import { getFavorites, addFavorite, removeFavorite } from "../../apiServices/favorites";
import { getVisits, createVisit, deleteVisit } from "../../apiServices/visits";
import { getLugar, getLugaresSimilares } from "../../apiServices/lugares";
import List from "../lista/List";

export default function LugarCard({ lugarId, onClose, setAlert, showComment, setShowComment, setLugarId }) {
  const { user } = useContext(AuthContext);

  const [lugar, setLugar] = useState(null);
  const [datosLugar, setDatosLugar] = useState(null);
  const [liked, setLiked] = useState(false);
  const [favorite, setFavorite] = useState(false);
  const [visited, setVisited] = useState(false);

  const [similares, setSimilares] = useState([]);

  const [cargandoSimilares, setCargandoSimilares] = useState(false);

  const tipoMap = {
    "PU": "Parque urbano",
    "PN": "Parque no urbano",
    "PI": "Parque infantil (con uso infantil sólo)",
    "JA": "Jardines",
    "AN": "Áreas de la naturaleza",
    "RF": "Refugios de pesca y de montaña",
    "CA": "Campamentos",
    "ZR": "Zonas recreativas naturales",
    "OT": "Otros",
    "LO": "Lonja",
    "ME": "Mercado",
    "FE": "Feria"
  };

  useEffect(() => {
    if (!lugarId) return;

    const fetchData = async () => {
      try {
        const lugarRes = await getPlace(lugarId);
        setLugar(lugarRes.data);
        const datosRes = await getLugar(lugarId);
        console.log("Datos del lugar:", datosRes);
        setDatosLugar(datosRes);

        const [likesRes, favRes, visitRes] = await Promise.all([
          getLikes(user.id),
          getFavorites(user.id),
          getVisits(user.id),
        ]);

        setLiked(likesRes.data.some(l => l.id === lugarId));
        setFavorite(favRes.data.some(f => f.id === lugarId));
        setVisited(visitRes.data.some(v => v.id === lugarId));

      } catch (err) {
        console.error(err);
      }
    };

    fetchData();
  }, [lugarId, user, liked]);

  const handleVerSimilares = async () => {
    setCargandoSimilares(true);
    try {
      // Llamada al endpoint que procesa el CSV/Cluster
      const res = await getLugaresSimilares(lugarId);

      const features = res.features || [];
      const lugaresSimilares = features.map((feature) => ({
        id: feature.properties.id,
        nombre: feature.properties.nombre,
        municipio: feature.properties.municipio,
        ...feature.properties,
      }));

      await console.log("Lugares similares obtenidos:", lugaresSimilares);

      setSimilares(lugaresSimilares);
    } catch (err) {
      setAlert?.({ title: "Error", message: "No se pudieron cargar lugares similares", type: 0 });
    } finally {
      setCargandoSimilares(false);
    }
  };

  // 🔘 handlers
  const handleLike = async () => {
    try {
      if (liked && user) {
        await unlike({ user_id: user.id, lugar_id: lugarId });
        setLiked(false);
      } else if (user) {
        await like({ user_id: user.id, lugar_id: lugarId });
        setLiked(true);
      }
      else {
        setAlert?.({ title: "Aviso", message: "Debes iniciar sesión para dar like", type: 0 });
      }
    } catch {
      setAlert?.({ title: "Error", message: "Error en like", type: 0 });
    }
  };

  const handleFavorite = async () => {
    try {
      if (favorite && user) {
        await removeFavorite({ user_id: user.id, lugar_id: lugarId });
        setFavorite(false);
      } else if (user) {
        await addFavorite({ user_id: user.id, lugar_id: lugarId });
        setFavorite(true);
      }
      else {
        setAlert?.({ title: "Aviso", message: "Debes iniciar sesión para agregar a favoritos", type: 0 });
      }
    } catch {
      setAlert?.({ title: "Error", message: "Error en favoritos", type: 0 });
    }
  };

  const handleVisit = async () => {
    try {
      if (visited && user) {
        await deleteVisit({ user_id: user.id, lugar_id: lugarId });
        setVisited(false);
      } else if (user) {
        await createVisit({ user_id: user.id, lugar_id: lugarId });
        setVisited(true);
      }
      else {
        setAlert?.({ title: "Aviso", message: "Debes iniciar sesión para marcar como visitado", type: 0 });
      }
    } catch {
      setAlert?.({ title: "Error", message: "Error en visitas", type: 0 });
    }
  };

  if (!lugar) return null;
  if (!datosLugar) return <p>Cargando datos del sitio...</p>;
  const feature = datosLugar.features[0];
  const info = feature.properties;

  return (
    <div className="lugar-card">
      <button className="close-btn" onClick={onClose}>✖</button>

      <div className="lugar-content">
        <br />
        <h3 className="lugar-title">{lugar.name}</h3>
        <h4 className="lugar-title">{info.municipio}</h4>

        {/* ⭐ info principal (NO TOCADA) */}
        <div className="lugar-meta">
          <span>⭐ {lugar.media != null ? Number(lugar.media).toFixed(1) : "N/A"}</span>
          <span>❤️ {lugar.likes ?? 0}</span>
        </div>

        {/* 🧾 info */}
        <div className="lugar-info">
          <span>{tipoMap[lugar.tipo]}</span>
          <span className={`estado estado-${lugar.estado}`}>
            {lugar.estado}
          </span>
        </div>

        {/* 🔧 extras */}
        <div className="lugar-extra">
          {lugar.accesible && <span>♿</span>}
          {lugar.agua && <span>💧</span>}
          {lugar.juegos && <span>🎮</span>}
          {lugar.comedor && <span>🍽️</span>}
          {lugar.electricidad && <span>⚡</span>}
        </div>

        <div>
          {info.superficie_cubierta !== 0 && (
            <p>🗺️ Superficie cubierta: {info.superficie_cubierta} m²</p>
          )}
        </div>

        {/* 🔥 NUEVO: acciones */}
        <div className="lugar-actions">
          <button
            className={liked ? "active" : ""}
            onClick={handleLike}
          >
            ❤️
          </button>

          <button
            className={favorite ? "active" : ""}
            onClick={handleFavorite}
          >
            ⭐
          </button>

          <button
            className={visited ? "active" : ""}
            onClick={handleVisit}
          >
            👁️
          </button>
        </div>

        {/* SECCIÓN DE LUGARES SIMILARES */}
        <div style={{ marginTop: "1rem" }}>

          {similares.length === 0 ? (
            <button
              className="comentarios-btn"
              onClick={handleVerSimilares}
              disabled={cargandoSimilares}
              style={{ width: "100%", marginTop: "0.5rem" }}
            >
              {cargandoSimilares ? "Analizando clúster..." : "Ver lugares similares 🔍"}
            </button>
          ) : (
            <div style={{ marginTop: "0.5rem" }}>
              <b>Lugares Similares</b>
              <List items={similares} setLugarId={setLugarId} />

              {/* Botón para cerrar los similares */}
              <button
                className="comentarios-btn"
                onClick={() => setSimilares([])}
                style={{
                  width: "100%",
                  marginTop: "0.5rem",
                  backgroundColor: "#6c757d" // Un tono gris para diferenciarlo
                }}
              >
                Ocultar similares ⬆️
              </button>
            </div>
          )}
        </div>

        {!showComment && (
          <button className="comentarios-btn" onClick={() => setShowComment(true)}>
            Ver comentarios ⬇️
          </button>
        )}

        {showComment && (
          <button className="comentarios-btn" onClick={() => setShowComment(false)}>
            Cerrar comentarios ⬆️
          </button>
        )}
      </div>
    </div>
  );
}