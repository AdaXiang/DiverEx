import { useEffect, useState, useContext } from "react";
import "./LugarCard.css";

import { AuthContext } from "../../context/AuthContext";

import { getPlace } from "../../apiServices/placesInfo";
import { getLikes, like, unlike } from "../../apiServices/likes";
import { getFavorites, addFavorite, removeFavorite } from "../../apiServices/favorites";
import { getVisits, createVisit, deleteVisit } from "../../apiServices/visits";

export default function LugarCard({ lugarId, onClose, setAlert, showComment, setShowComment }) {
  const { user } = useContext(AuthContext);

  const [lugar, setLugar] = useState(null);

  const [liked, setLiked] = useState(false);
  const [favorite, setFavorite] = useState(false);
  const [visited, setVisited] = useState(false);

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

  return (
    <div className="lugar-card">
      <button className="close-btn" onClick={onClose}>✖</button>

      {/* imagen */}
      {/* <div className="lugar-img" /> */}

      <div className="lugar-content">
        <h3 className="lugar-title">{lugar.name}</h3>

        {/* ⭐ info principal (NO TOCADA) */}
        <div className="lugar-meta">
          <span>⭐ {lugar.media ?? "N/A"}</span>
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