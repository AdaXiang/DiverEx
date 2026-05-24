import "./Item.css";
export default function Item({ data, setLugarId }) {
    console.log("DATA ITEM:", data);

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
        accesible,
        acceso_silla_ruedas,
        distancia_km
    } = data;

    const esAccesible =
        accesible ??
        acceso_silla_ruedas ??
        false;

    return (
        <div className="item" onClick={() => setLugarId(id)}>
            <div className="item-header">
                <span className="item-name">{nombre ?? name ?? "Sin nombre"}</span>
                <span className="item-tipo">{tipoMap[tipo] ?? tipoMap[tipo_lugar]}</span>
            </div>

            <p className="item-municipio">{municipio}</p>

            {distancia_km != null && (
                <p className="item-municipio">
                    {distancia_km < 1 ? `${Math.round(distancia_km * 1000)} m` : `${distancia_km} km`}
                </p>
            )}

            <div className="item-body">
                <span className={`estado estado-${estado}`}>
                    {estadoMap[estado]}
                </span>

                <span className={`accesible ${esAccesible ? "yes" : "no"}`}>
                    {esAccesible ? "Accesible" : "No accesible"}
                </span>
            </div>

            {/* <div className="item-footer">
                <span className="item-id">{id}</span>
            </div> */}
        </div>
    );
}
