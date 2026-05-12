// MapView.jsx
import { useState } from "react";
import { MapContainer, TileLayer, useMap } from "react-leaflet";
import GeoJSONLayer from "./GeoJSONLayer";
import LocationMarker from "./LocationMarker";
import Filtros from "../filtros/Filtros";
import "./MapView.css";

import "leaflet/dist/leaflet.css";

function BotonCentrar({ userLocation }) {
    const map = useMap();

    const centrarMapa = () => {
        if (userLocation) {
            map.flyTo([userLocation.lat, userLocation.lng], 16, {
                animate: true,
                duration: 1.5 // Segundos que tarda la animación
            });
        }
    };

    // Si aún no tenemos la ubicación, no mostramos el botón
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

export default function MapView({ setUserLocation, filters, userLocation, setLugarId }) {

    return (
        <div style={{ position: "relative", width: "100%", height: "100vh", overflow: "hidden" }}>

            {/* MAPA */}
            <MapContainer
                center={[38.956, -5.861]}
                zoom={13}
                style={{ height: "100%", width: "100%", zIndex: 1 }}
                preferCanvas={true}
            >
                <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />


                <GeoJSONLayer filters={filters} userLocation={userLocation} setLugarId={setLugarId} />
                <LocationMarker setUserLocation={setUserLocation} />
                <BotonCentrar userLocation={userLocation} />
            </MapContainer>
        </div>
    );
}