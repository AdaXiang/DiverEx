import { useState, useContext } from "react";
import "./LoginModal.css";
import { login, signup } from "../../apiServices/users";
import { AuthContext } from "../../context/AuthContext";

export default function AuthModal({ setAlert }) {
  const { loginUser } = useContext(AuthContext);

  // Formulario base
  const [form, setForm] = useState({
    email: "",
    password: "",
    name: "",
  });

  // modo login / registro
  const [isLogin, setIsLogin] = useState(true);

  // minimizar panel
  const [minimized, setMinimized] = useState(false);

  // submit
  const handleSubmit = async () => {
    try {
      let res;

      if (isLogin) {
        res = await login(form);
      } else {
        res = await signup(form);
      }

      loginUser(res.data);

      // ✅ alerta global
      setAlert({
        title: "Correcto",
        message: isLogin
          ? "Inicio de sesión correcto"
          : "Cuenta creada correctamente",
        type: 2,
      });

    } catch (err) {
      console.error(err);

      setAlert({
        title: "Error",
        message:
          err.response?.data?.detail ||
          "Credenciales incorrectas o error en el servidor",
        type: 0,
      });
    }
  };

  // login invitado
  const handleGuestLogin = () => {
    loginUser({
      id: "0",
      name: "Invitado",
    });

    setAlert({
      title: "Bienvenido",
      message: "Has entrado como invitado",
      type: 1,
    });
  };

  // render
  return minimized ? (
    <div
      id="loginup"
      className="minimized"
      onClick={() => setMinimized(false)}
    >
      🗝️ Iniciar sesión
    </div>
  ) : (
    <div id="loginup">
      <button
        className="minimize-btn"
        onClick={() => setMinimized(true)}
      >
        ⬆
      </button>

      <h2>{isLogin ? "Iniciar sesión" : "Registrarse"}</h2>

      {!isLogin && (
        <input
          placeholder="nombre"
          onChange={(e) =>
            setForm({ ...form, name: e.target.value })
          }
        />
      )}

      <input
        placeholder="email"
        onChange={(e) =>
          setForm({ ...form, email: e.target.value })
        }
      />

      <input
        type="password"
        placeholder="password"
        onChange={(e) =>
          setForm({ ...form, password: e.target.value })
        }
      />

      <button onClick={handleSubmit}>
        {isLogin ? "Entrar" : "Crear cuenta"}
      </button>

      {isLogin && (
        <button onClick={handleGuestLogin}>
          Iniciar sesión Google
        </button>
      )}

      <button
        className="secondary-btn"
        onClick={() => setIsLogin(!isLogin)}
      >
        {isLogin
          ? "¿No tienes cuenta? Regístrate"
          : "¿Ya tienes cuenta? Inicia sesión"}
      </button>
    </div>
  );
}