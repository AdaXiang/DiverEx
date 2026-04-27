import { useEffect, useState } from "react";
import { GeoJSON } from "react-leaflet";

export default function GeoJSONLayer() {
    const [data, setData] = useState(null);

    useEffect(() => {
        fetch("/parques2025.geojson") // cambiar por llamada a API 
            .then((res) => res.json())
            .then((geojson) => {
                console.log("GeoJSON cargado:", geojson);
                setData(geojson);
            })
            .catch((err) => console.error("Error cargando GeoJSON:", err));
    }, []);

    if (!data) return null;

    const style = (feature) => {
        return {
            color: "green",
            fillColor: "green",
            fillOpacity: 0.4,
            weight: 2
        };
    };

    const onEachFeature = (feature, layer) => {
        if (feature.properties?.nombre) {
            layer.bindPopup(feature.properties.nombre);
        }
    };

    return <GeoJSON data={data} style={style} onEachFeature={onEachFeature} />;
}