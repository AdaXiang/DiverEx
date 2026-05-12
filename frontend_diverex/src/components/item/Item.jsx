import "./Item.css";
export default function Item({ data, setLugarId }) {

    const tipoMap = {
        "PU": "Parque urbano",
        "PN": "Parque no urbano",
        "PI": "Parque infantil",
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

    const estadoMap = {
        B: "Bueno",
        M: "Mantenimiento",
        R: "Reparación"
    };

    const {
        id,
        name,
        nombre,
        tipo,
        tipo_lugar,
        municipio,
        estado,
        accesible
    } = data;

    return (
        <div className="item" onClick={() => setLugarId(data.id)}>
            <div className="item-header">
                <span className="item-name">{nombre ?? name ?? "Sin nombre"}</span>
                <span className="item-tipo">{tipoMap[tipo] ?? tipoMap[tipo_lugar]}</span>
            </div>

            <p className="item-municipio">{municipio}</p>

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
