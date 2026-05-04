import { useEffect, useState, useContext } from "react";
import "./ComentariosPanel.css";

import { getCommentsByPlace, createComment } from "../../apiServices/comments";
import { AuthContext } from "../../context/AuthContext";

export default function ComentariosPanel({ lugarId, onClose }) {
  const { user } = useContext(AuthContext);

  const [comentarios, setComentarios] = useState([]);
  const [mensaje, setMensaje] = useState("");
  const [ranking, setRanking] = useState(3);

  useEffect(() => {
    if (!lugarId) return;

    const fetchComentarios = async () => {
      try {
        const res = await getCommentsByPlace(lugarId);
        setComentarios(res.data);
      } catch (err) {
        console.error(err);
      }
    };

    fetchComentarios();
  }, [lugarId]);

  const handleSubmit = async () => {
    if (!mensaje) return;

    try {
      const nuevo = {
        user_id: user.id,
        lugar_id: lugarId,
        mensaje,
        ranking,
      };

      await createComment(nuevo);

      // refrescar
      setComentarios((prev) => [...prev, nuevo]);

      setMensaje("");
      setRanking(3);

    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="comentarios-panel">
      <button className="close-btn" onClick={onClose}>✖</button>

      <h3>Comentarios</h3>

      {/* lista */}
      <div className="comentarios-list">
        {comentarios.length === 0 && <p>No hay comentarios</p>}

        {comentarios.map((c, i) => (
          <div key={i} className="comentario">
            <span className="comentario-msg">{c.mensaje}</span>
            <span className="comentario-rank">⭐ {c.ranking}</span>
          </div>
        ))}
      </div>

      {/* crear */}
      {user && (
        <div className="comentario-form">
          <input
            placeholder="Escribe un comentario..."
            value={mensaje}
            onChange={(e) => setMensaje(e.target.value)}
          />

          <input
            type="number"
            min="1"
            max="5"
            value={ranking}
            onChange={(e) => setRanking(e.target.value)}
          />

          <button onClick={handleSubmit}>
            Enviar
          </button>
        </div>
      )}
    </div>
  );
}