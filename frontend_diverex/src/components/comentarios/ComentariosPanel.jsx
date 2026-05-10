import { useEffect, useState, useContext } from "react";
import "./ComentariosPanel.css";

import {
  getCommentsByPlace,
  createComment,
  deleteComment,
  getCommentsByUser
} from "../../apiServices/comments";

import { AuthContext } from "../../context/AuthContext";

export default function ComentariosPanel({
  lugarId,
  setAlert,
}) {
  const { user } = useContext(AuthContext);

  const [comentarios, setComentarios] = useState([]);
  const [myComment, setMyComment] = useState(null);

  // popup crear / editar
  const [showForm, setShowForm] = useState(false);

  const [mensaje, setMensaje] = useState("");
  const [ranking, setRanking] = useState(3);

  // filtro ranking
  const [rankingFilterMin, setRankingFilterMin] = useState(1);
  const [rankingFilterMax, setRankingFilterMax] = useState(5);

  // cargar comentarios
  useEffect(() => {
    if (!lugarId) return;

    const fetchComentarios = async () => {
      try {

        // comentarios del lugar con filtros backend
        const res = await getCommentsByPlace(
          lugarId,
          rankingFilterMin,
          rankingFilterMax
        );

        setComentarios(res.data);

        // comentario del usuario
        if (user) {

          const userCommentsRes =
            await getCommentsByUser(user.id);

          const comentarioUsuario =
            userCommentsRes.data.find(
              (c) => c.lugar?.id === lugarId
            );

          setMyComment(comentarioUsuario || null);
        }

      } catch (err) {
        console.error(err);

        setAlert?.({
          title: "Error",
          message: "No se pudieron cargar los comentarios",
          type: 0,
        });
      }
    };

    fetchComentarios();

  }, [
    lugarId,
    rankingFilterMin,
    rankingFilterMax,
    user,
    setAlert
  ]);

  // abrir popup
  const handleOpenForm = () => {

    if (myComment) {
      setMensaje(myComment.mensaje);
      setRanking(myComment.ranking);
    } else {
      setMensaje("");
      setRanking(3);
    }

    setShowForm(true);
  };

  // crear / editar comentario
  const handleSubmit = async () => {

    if (!mensaje.trim()) return;

    try {

      const comentarioData = {
        user_id: user.id,
        lugar_id: lugarId,
        mensaje,
        ranking,
      };

      // backend hace UPSERT
      await createComment(comentarioData);

      // recargar comentarios filtrados
      const res = await getCommentsByPlace(
        lugarId,
        rankingFilterMin,
        rankingFilterMax
      );

      setComentarios(res.data);

      // actualizar comentario propio
      const nuevoMyComment = {
        ...comentarioData,
        id: `${user.id}_${lugarId}`,
        fecha: new Date().toISOString(),
        usuario: {
          id: user.id,
          name: user.name,
        },
        lugar: {
          id: lugarId,
        }
      };

      setMyComment(nuevoMyComment);

      setShowForm(false);

      setAlert?.({
        title: "Correcto",
        message: myComment
          ? "Comentario actualizado"
          : "Comentario añadido",
        type: 2,
      });

    } catch (err) {
      console.error(err);

      setAlert?.({
        title: "Error",
        message: "No se pudo guardar el comentario",
        type: 0,
      });
    }
  };

  // eliminar comentario
  const handleDelete = async () => {

    try {

      await deleteComment({
        user_id: user.id,
        lugar_id: lugarId,
      });

      // quitar comentario de la lista
      setComentarios((prev) =>
        prev.filter(
          (c) => c.usuario?.id !== user.id
        )
      );

      // limpiar comentario usuario
      setMyComment(null);

      // limpiar popup
      setMensaje("");
      setRanking(3);

      setShowForm(false);

      setAlert?.({
        title: "Correcto",
        message: "Comentario eliminado",
        type: 2,
      });

    } catch (err) {
      console.error(err);

      setAlert?.({
        title: "Error",
        message: "No se pudo eliminar el comentario",
        type: 0,
      });
    }
  };

  return (
    <div className="comentarios-panel">

      {/* HEADER */}
      <div className="comentarios-header">

        <h4>
          Comentarios ({comentarios.length})
        </h4>

        <div className="comentarios-header-actions">

          {/* filtro min */}
          <select
            value={rankingFilterMin}
            onChange={(e) => {

              const value = Number(e.target.value);

              setRankingFilterMin(value);

              // evitar min > max
              if (value > rankingFilterMax) {
                setRankingFilterMax(value);
              }
            }}
          >

            <option value={1}>1⭐</option>
            <option value={2}>2⭐</option>
            <option value={3}>3⭐</option>
            <option value={4}>4⭐</option>
            <option value={5}>5⭐</option>

          </select>

          {/* filtro max */}
          <select
            value={rankingFilterMax}
            onChange={(e) =>
              setRankingFilterMax(
                Number(e.target.value)
              )
            }
          >

            <option
              value={1}
              disabled={1 < rankingFilterMin}
            >
              1⭐
            </option>

            <option
              value={2}
              disabled={2 < rankingFilterMin}
            >
              2⭐
            </option>

            <option
              value={3}
              disabled={3 < rankingFilterMin}
            >
              3⭐
            </option>

            <option
              value={4}
              disabled={4 < rankingFilterMin}
            >
              4⭐
            </option>

            <option
              value={5}
              disabled={5 < rankingFilterMin}
            >
              5⭐
            </option>

          </select>

        </div>

        <div className="comentarios-header-actions">

          {/* crear / editar */}
          {user && (
            <button
              className="nuevo-comentario-btn"
              onClick={handleOpenForm}
            >
              {myComment
                ? "✏️ Editar"
                : "✍️ Añadir"}
            </button>
          )}

        </div>
      </div>

      {/* LISTA */}
      <div className="comentarios-list">

        {comentarios.length === 0 && (
          <span className="no-comments">
            No hay comentarios
          </span>
        )}

        {comentarios.map((c) => (

          <div
            key={c.id}
            className={`comentario ${
              c.usuario?.id === user?.id
                ? "my-comment"
                : ""
            }`}
          >

            <div className="comentario-top">

              <span className="comentario-user">
                👤 {c.usuario?.name}
              </span>

              <span className="comentario-ranking">
                {"⭐".repeat(c.ranking)}
              </span>

            </div>

            <div className="comentario-msg">
              {c.mensaje}
            </div>

            <div className="comentario-date">
              {new Date(c.fecha).toLocaleDateString()}
            </div>

          </div>
        ))}

      </div>

      {/* POPUP */}
      {showForm && (
        <div className="comentario-popup">

          <h4>
            {myComment
              ? "Editar comentario"
              : "Nuevo comentario"}
          </h4>

          <textarea
            placeholder="Escribe tu comentario..."
            value={mensaje}
            onChange={(e) =>
              setMensaje(e.target.value)
            }
          />

          <div className="popup-actions">

            <select
              value={ranking}
              onChange={(e) =>
                setRanking(Number(e.target.value))
              }
            >
              <option value={1}>1 ⭐</option>
              <option value={2}>2 ⭐</option>
              <option value={3}>3 ⭐</option>
              <option value={4}>4 ⭐</option>
              <option value={5}>5 ⭐</option>
            </select>

            <button
              className="save-btn"
              onClick={handleSubmit}
            >
              Guardar
            </button>

            {myComment && (
              <button
                className="delete-btn"
                onClick={handleDelete}
              >
                Eliminar
              </button>
            )}

            <button
              className="cancel-btn"
              onClick={() =>
                setShowForm(false)
              }
            >
              Cancelar
            </button>

          </div>
        </div>
      )}

    </div>
  );
}