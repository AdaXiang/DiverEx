import "./List.css";
import Item from "../item/Item";

export default function List({ items, setLugarId }) {
  if (!items || items.length === 0) {
    return <p className="empty">No hay datos, interactua más por la pagina :D </p>;
  }

  return (
    <div className="list">
      {items.map((item, index) => (
        <Item key={index} data={item} setLugarId={setLugarId} />
      ))}
    </div>
  );
}