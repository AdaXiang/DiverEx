import { useEffect, useMemo } from "react";
import { MapContainer, TileLayer, useMap } from "react-leaflet";
import GeoJSONLayer from "./GeoJSONLayer";
import LocationMarker from "./LocationMarker";
import "./MapView.css";
import "leaflet/dist/leaflet.css";

function BotonCentrar({ userLocation }) {
    const map = useMap();

    const centrarMapa = () => {
        if (userLocation) {
            map.flyTo([userLocation.lat, userLocation.lng], 16, {
                animate: true,
                duration: 1.5
            });
        }
    };

    if (!userLocation) return null;

    return (
        <button
            className="btn-centrar-mapa"
            onClick={centrarMapa}
            title="Centrar en mi ubicación"
        >
            📍 Centrar
        </button>
    );
}

function MapController({ selectedFeature }) {
    const map = useMap();

    useEffect(() => {
        if (selectedFeature && selectedFeature.coords) {
            const [lon, lat] = selectedFeature.coords;
            console.log("Volando a:", lat, lon); // Para que veas en consola si se ejecuta

            map.flyTo([lat, lon], 18, {
                animate: true,
                duration: 1.5,
            });
        }
    }, [selectedFeature, map]);

    return null;
}

export default function MapView({
    setUserLocation,
    filters,
    modoFiltro,
    recommendationFilters,
    userLocation,
    setLugarId,
    setLugaresFiltrados,
    lugaresFiltrados,
    lugarId
}) {

    const selectedFeature = useMemo(() => {
        if (!lugarId || !lugaresFiltrados) return null;

        // Buscamos el objeto en la lista
        const item = lugaresFiltrados.find(f => (f.id === lugarId || f.properties?.id === lugarId));

        if (!item) return null;

        return {
            coords: item.geo_point?.coordinates || item.coordinates
        };
    }, [lugarId, lugaresFiltrados]);

    return (
        <div style={{ position: "relative", width: "100%", height: "100vh", overflow: "hidden" }}>
            <MapContainer
                center={[38.956, -5.861]}
                zoom={13}
                style={{ height: "100%", width: "100%", zIndex: 1 }}
            >
                <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

                {/* Pasamos el objeto normalizado con las coordenadas */}
                <MapController selectedFeature={selectedFeature} />
                <GeoJSONLayer
                    filters={filters}
                    modoFiltro={modoFiltro}
                    recommendationFilters={recommendationFilters}
                    userLocation={userLocation}
                    setLugarId={setLugarId}
                    setLugaresFiltrados={setLugaresFiltrados} // Ahora este componente sí podrá llenar la lista
                    lugarId={lugarId}
                />


                <LocationMarker setUserLocation={setUserLocation} />
                <BotonCentrar userLocation={userLocation} />
            </MapContainer>
        </div>
    );
}