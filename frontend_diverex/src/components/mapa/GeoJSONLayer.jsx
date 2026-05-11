import { useEffect, useState, useMemo } from "react"; // 1. Importación añadida
import { GeoJSON, Marker, Popup } from "react-leaflet";
import MarkerClusterGroup from 'react-leaflet-cluster';

import L from 'leaflet';
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41]
});

L.Marker.prototype.options.icon = DefaultIcon;

const COLORES_DATASET = {
    "lonjas": "#2563eb",
    "parques": "#16a34a",
    "default": "#6b7280"
};

export default function GeoJSONLayer() {
    const [data, setData] = useState(null);

    // 2. Definición del 'style' usando useMemo para evitar recalculaciones innecesarias
    const style = useMemo(() => (feature) => {
        const tipo = feature.properties?.dataset;
        const color = COLORES_DATASET[tipo] || COLORES_DATASET.default;
        return {
            color: color,
            fillColor: color,
            fillOpacity: 0.2,
            weight: 2,
        };
    }, []);

    useEffect(() => {
        fetch("http://localhost:8001/api/lugares")
            .then((res) => res.json())
            .then((geojson) => setData(geojson))
            .catch((err) => console.error("Error:", err));
    }, []);

    // 3. El 'if' para esperar los datos va DESPUÉS de definir los Hooks
    if (!data) return null;
    return (
        <>
            <GeoJSON
                key={JSON.stringify(data)}
                data={data}
                style={style}
            />

            <MarkerClusterGroup chunkedLoading>
                {data.features.map((feature, index) => {
                    const coordinates = feature.geo_point?.coordinates;

                    if (coordinates && coordinates.length === 2) {
                        const [lon, lat] = coordinates;

                        return (
                            <Marker
                                key={feature.id || index}
                                position={[lat, lon]} // Leaflet usa [lat, lon]
                            >
                                <Popup>
                                    <strong>{feature.properties?.nombre}</strong>
                                    <br />
                                    {feature.properties?.municipio}
                                </Popup>
                            </Marker>
                        );
                    }

                    return null;
                })}
            </MarkerClusterGroup>
        </>
    );
}