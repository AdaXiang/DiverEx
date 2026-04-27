import { MapContainer, TileLayer } from "react-leaflet";
import GeoJSONLayer from "./GeoJSONLayer";
import "leaflet/dist/leaflet.css";

export default function MapView() {
    return (
        <MapContainer
            center={[38.956, -5.861]}
            zoom={13}
            style={{ height: "100vh", width: "100%" }}
        >
            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

            <GeoJSONLayer />
        </MapContainer>
    );
}