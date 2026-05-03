import "./Item.css";
export default function Item({ data , setLugarId}) {

    const tipoMap = {
        ME: "Mercado",
        FE: "Ferial",
        PU: "Parque",
        PI: "Parque infantil",
        JA: "Jardín",
        ZR: "Zona recreativa"
    };

    const estadoMap = {
        B: "Bueno",
        M: "Mantenimiento",
        R: "Reparación"
    };

    const {
        id,
        name,
        tipo,
        estado,
        accesible
    } = data;

    return (
        <div className="item" onClick={() => setLugarId(data.id)}>
            <div className="item-header">
                <span className="item-name">{name}</span>
                <span className="item-tipo">{tipoMap[tipo]}</span>
            </div>

            <div className="item-body">
                <span className={`estado estado-${estado}`}>
                {estadoMap[estado]}
                </span>

                <span className={`accesible ${accesible ? "yes" : "no"}`}>
                {accesible ? "Accesible" : "No accesible"}
                </span>
            </div>

            {/* <div className="item-footer">
                <span className="item-id">{id}</span>
            </div> */}
        </div>
    );
}
