import { useContext, useState, useEffect } from "react";
import "./UserPanel.css";
import { AuthContext } from "../../context/AuthContext";
import List from "../lista/List";

import { getFavorites } from "../../apiServices/favorites";
import { getLikes } from "../../apiServices/likes";
import { getVisits } from "../../apiServices/visits";
import { deleteUser } from "../../apiServices/users";

export default function UserPanel({ setAlert , setLugarId}) {
  const { user, logout } = useContext(AuthContext);

  const [mode, setMode] = useState(0);
  const [data, setData] = useState([]);

  const handleModeChange = (newMode) => {
    setMode((prev) => (prev === newMode ? 0 : newMode));
  };

  useEffect(() => {
    if (!user || mode === 0) {
      setData([]);
      return;
    }

    const fetchData = async () => {
      try {
        let res;

        if (mode === 1) res = await getFavorites(user.id);
        if (mode === 2) res = await getLikes(user.id);
        if (mode === 3) res = await getVisits(user.id);

        setData(res.data);
      } catch (err) {
        console.error(err);
      }
    };

    fetchData();
  }, [mode, user]);

  const handleLogoutAccount = () => {
      setAlert({
        title: "Cierre sesion",
        message:"Hasta la proxima",
        type: 2,
      });

      logout(); // limpia sesión
  }


  // eliminar cuenta
  const handleDeleteAccount = async () => {
    const confirmDelete = window.confirm(
      "¿Seguro que quieres eliminar tu cuenta? Esta acción es irreversible."
    );

    if (!confirmDelete) return;

    try {
      await deleteUser(user.id);

      setAlert({
        title: "Correcto",
        message:"Cuenta eliminada",
        type: 1,
      });

      logout(); // limpia sesión
    } catch (err) {
      console.error(err);

      setAlert({
        title: "Fallo",
        message:"Se produjo un error en el servidor",
        type: 2,
      });
    }
  };

  return (
    <div id="userPanel">
      <span className="user-name">{user?.name}</span>

      <div className="menu">
        <button
          className={mode === 1 ? "active" : ""}
          onClick={() => handleModeChange(1)}
        >
          ⭐ Favoritos
        </button>

        <button
          className={mode === 2 ? "active" : ""}
          onClick={() => handleModeChange(2)}
        >
          💙 Likes
        </button>

        <button
          className={mode === 3 ? "active" : ""}
          onClick={() => handleModeChange(3)}
        >
          📌 Visitas
        </button>
      </div>

      {mode !== 0 && <List items={data} setLugarId={setLugarId} />}

      <div className="menu">
        <button className="logout-btn" onClick={handleLogoutAccount}>
          Cerrar sesión
        </button>

        <button className="delete-btn" onClick={handleDeleteAccount}>
          Eliminar cuenta
        </button>
      </div>
      
    </div>
  );
}