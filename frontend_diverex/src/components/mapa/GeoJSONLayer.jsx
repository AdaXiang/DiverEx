import { useEffect, useState, useMemo } from "react";
import { GeoJSON, Marker, Popup, useMap } from "react-leaflet";
import MarkerClusterGroup from 'react-leaflet-cluster';
import { getLugaresFiltrados } from "../../apiServices/lugares.js";

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

export default function GeoJSONLayer({ filters, userLocation, setLugarId, setLugaresFiltrados }) {
    const map = useMap();
    const [data, setData] = useState(null);

    const centrarMapa = (lat, lon) => {
        map.flyTo([lat, lon], 16, {
            animate: true,
            duration: 1.5
        });
    };

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
        const fetchDatosFiltrados = async () => {
            try {
                const geojson = await getLugaresFiltrados({
                    ...filters,
                    lat: userLocation?.lat,
                    lon: userLocation?.lng
                });

                setData(geojson);

                if (setLugaresFiltrados && geojson.features) {
                    //const datosParaLista = geojson.features.map(f => f.properties);
                    const datosParaLista = geojson.features.map(f => ({
                        ...f.properties,
                        coordinates: f.geo_point?.coordinates // Guardamos las coordenadas explícitamente
                    }));
                    setLugaresFiltrados(datosParaLista);
                }

            } catch (error) {
                console.error("Error en servidor:", error);

                if (error.response) {
                    console.error("Status:", error.response.status);
                    console.error("Body:", error.response.data);
                }

                setData({
                    type: "FeatureCollection",
                    features: []
                });
            }
        };

        const timer = setTimeout(() => {
            fetchDatosFiltrados();
        }, 400);

        return () => clearTimeout(timer);

    }, [filters, userLocation]);


    if (!data) return null;

    if (data.features && data.features.length === 0) {
        console.log("No hay resultados para estos filtros.");
    }

    return (
        <>
            <GeoJSON
                key={JSON.stringify(data)}
                data={data}
                style={style}
            />

            <MarkerClusterGroup chunkedLoading>
                {data.features?.map((feature, index) => {
                    const coordinates = feature.geo_point?.coordinates;

                    if (coordinates && coordinates.length === 2) {
                        const [lon, lat] = coordinates;

                        return (
                            <Marker
                                key={feature.id || index}
                                position={[lat, lon]}
                                eventHandlers={{
                                    click: () => {
                                        // Centrar el mapa en la ubicación del marcador
                                        centrarMapa(lat, lon);

                                        if (feature.properties?.id) {
                                            setLugarId(feature.properties?.id);
                                        }
                                    }
                                }}
                            >
                                <Popup autoPan={false}>
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