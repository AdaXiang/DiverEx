import { useEffect, useState } from "react";
import "./Alert.css";

export default function Alert({ title, message, type = 2, onClose }) {
  const [visible, setVisible] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setVisible(false);

      // esperar animación antes de eliminar
      setTimeout(() => {
        onClose && onClose();
      }, 300);
    }, 3000);

    return () => clearTimeout(timer);
  }, []);

  if (!visible) return null;

  const getTypeClass = () => {
    switch (type) {
      case 0:
        return "alert error";
      case 1:
        return "alert warning";
      case 2:
      default:
        return "alert success";
    }
  };

  return (
    <div className={getTypeClass()}>
      <div className="alert-header">
        <strong>{title}</strong>
        <button onClick={() => setVisible(false)}>✖</button>
      </div>
      <p>{message}</p>
    </div>
  );
}