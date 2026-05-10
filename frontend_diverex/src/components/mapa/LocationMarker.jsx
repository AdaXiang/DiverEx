import { useState, useEffect } from "react";
import { Marker, Popup, useMap } from "react-leaflet";
import L from "leaflet";

const redIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

// Añadimos una prop: setUserLocation
export default function LocationMarker({ setUserLocation }) {
    const [position, setPosition] = useState(null);
    const map = useMap();

    useEffect(() => {
        map.locate().on("locationfound", function (e) {
            setPosition(e.latlng);
            setUserLocation(e.latlng); // Le pasamos las coordenadas al padre
            console.log("Ubicación encontrada:", e.latlng);
            map.flyTo(e.latlng, map.getZoom());
        });
    }, [map, setUserLocation]);

    return position === null ? null : (
        <Marker position={position} icon={redIcon}>
            <Popup>¡Estás aquí!</Popup>
        </Marker>
    );
}