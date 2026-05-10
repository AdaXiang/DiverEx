import React from 'react';
import './Filtros.css';

export default function Filtros({ filters, setFilters, userLocation }) {
    return (
        <div className="filtros-panel-estatico">
            <h2>Filtros</h2>

            {/* Filtro Silla de Ruedas */}
            <label className="filtro-item">
                <input
                    type="checkbox"
                    checked={filters.sillaRuedas}
                    onChange={(e) => setFilters({ ...filters, sillaRuedas: e.target.checked })}
                />
                Accesible Silla de Ruedas
            </label>

            {/* Filtro Distancia */}
            <div className="filtro-grupo">
                <label>
                    Distancia máxima: <strong>{filters.distanciaMax} km</strong>
                </label>
                <input
                    type="range"
                    min="1" max="150" step="1"
                    value={filters.distanciaMax}
                    onChange={(e) => setFilters({ ...filters, distanciaMax: Number(e.target.value) })}
                    disabled={!userLocation}
                />

                {/* Mensaje si el GPS aún no ha respondido */}
                {userLocation ? (
                    <p className="mensaje-informativo">
                        Coordenadas: {userLocation.lat.toFixed(4)}, {userLocation.lng.toFixed(4)}
                    </p>
                ) : (
                    <span className="mensaje-error">Calculando tu ubicación...</span>
                )}
            </div>
        </div>
    );
}