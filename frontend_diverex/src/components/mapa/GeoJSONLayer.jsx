import { useEffect, useState, useMemo } from "react";
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

// 1. AHORA RECIBIMOS LOS FILTROS Y LA UBICACIÓN COMO PROPS
export default function GeoJSONLayer({ filters, userLocation, setLugarId }) {
    const [data, setData] = useState(null);

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

    // 2. EL EFECTO QUE REACCIONA A LOS FILTROS
    useEffect(() => {
        const fetchDatosFiltrados = async () => {
            const params = new URLSearchParams();

            // Filtros booleanos
            if (filters.sillaRuedas) params.append('acceso_silla_ruedas', 'true');
            if (filters.zonaInfantil) params.append('zona_infantil', 'true');
            if (filters.comedor) params.append('comedor', 'true');

            // Filtro espacial
            if (userLocation) {
                params.append('lat', userLocation.lat);
                params.append('lon', userLocation.lng);
                params.append('distancia_max', filters.distanciaMax);
            }

            // Filtros múltiples (Arrays)
            if (filters.estadosSeleccionados) {
                filters.estadosSeleccionados.forEach(e => params.append('estado', e));
            }
            if (filters.tiposSeleccionados) {
                filters.tiposSeleccionados.forEach(t => params.append('tipo_lugar', t));
            }

            // Filtros de Texto Inteligentes (Lugar, Municipio)
            if (filters.busquedaTexto) {
                const texto = filters.busquedaTexto;

                // Si el usuario escribe una coma (Ej: "Parque, Mérida")
                if (texto.includes(',')) {
                    const partes = texto.split(','); // Divide en ["Parque", " Mérida"]
                    const lugar = partes[0].trim();
                    const muni = partes[1].trim();

                    if (lugar) params.append('nombre', lugar);
                    if (muni) params.append('municipio', muni);
                }
                // Si no hay coma, asumimos que está buscando el nombre del sitio
                else {
                    params.append('nombre', texto.trim());
                }
            }

            try {
                // Hacemos fetch a la nueva ruta de filtros
                const url = `http://localhost:8001/api/lugares/filtrar?${params.toString()}`;
                console.log("Pidiendo a BD:", url); // <--- Te ayudará a ver qué se envía

                const res = await fetch(url);
                if (res.ok) {
                    const geojson = await res.json();
                    setData(geojson);
                } else {
                    console.error("Error en servidor:", res.status);
                    setData({ type: "FeatureCollection", features: [] }); // Evitar roturas
                }
            } catch (err) {
                console.error("Error de conexión:", err);
            }
        };

        // Ponemos un pequeño retraso (debounce) de 400ms. 
        // Si el usuario mueve el slider muy rápido, solo hacemos 1 petición al final.
        const timer = setTimeout(() => {
            fetchDatosFiltrados();
        }, 400);

        return () => clearTimeout(timer);

    }, [filters, userLocation]); // 3. EL EFECTO SE DISPARA CUANDO ESTO CAMBIA


    if (!data) return null;

    // Si la BD devuelve vacío, mostramos un mensaje por consola
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
                                        if (feature.properties?.id) {
                                            setLugarId(feature.properties?.id);
                                        }
                                    }
                                }}
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