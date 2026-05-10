// MapView.jsx
import { useState } from "react";
import { MapContainer, TileLayer } from "react-leaflet";
import GeoJSONLayer from "./GeoJSONLayer";
import LocationMarker from "./LocationMarker";
import Filtros from "../filtros/Filtros";

import "leaflet/dist/leaflet.css";

export default function MapView({ setUserLocation, filters, userLocation }) {
    // Los estados se quedan aquí para poder compartirlos entre Filtros y el Mapa
    console.log("Ubicación del usuario en MapView:", userLocation);

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

                <GeoJSONLayer filters={filters} userLocation={userLocation} />
                <LocationMarker setUserLocation={setUserLocation} />
            </MapContainer>
        </div>
    );
}