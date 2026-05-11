import React from 'react';
import './Filtros.css';

const opcionesTipo = {
    "Parques": [
        { id: "PU", label: "Parque urbano" },
        { id: "PN", label: "Parque no urbano" },
        { id: "PI", label: "Parque infantil" },
        { id: "JA", label: "Jardines" },
        { id: "AN", label: "Naturaleza" },
        { id: "ZR", label: "Zonas recreativas" },
    ],
    "Lonjas": [
        { id: "LO", label: "Lonja" },
        { id: "ME", label: "Mercado" },
        { id: "FE", label: "Feria" }
    ]
};

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

            {/* Filtro Zona Infantil */}
            <label className="filtro-item">
                <input
                    type="checkbox"
                    checked={filters.zonaInfantil}
                    onChange={(e) => setFilters({ ...filters, zonaInfantil: e.target.checked })}
                />
                Zona Infantil
            </label>

            {/* Filtro Comedor */}
            <label className="filtro-item">
                <input
                    type="checkbox"
                    checked={filters.comedor}
                    onChange={(e) => setFilters({ ...filters, comedor: e.target.checked })}
                />
                Comedor
            </label>

            {/* Filtro Estado - Tipo Segmentado */}
            <div className="filtro-grupo">
                <label className="filtro-label">Estado de conservación</label>
                <div className="toggle-container">
                    {[
                        { id: 'B', label: 'B', color: '#2ecc71' }, // Verde
                        { id: 'R', label: 'R', color: '#f1c40f' }, // Amarillo
                        { id: 'M', label: 'M', color: '#e74c3c' }, // Rojo
                        { id: 'E', label: 'E', color: '#3498db' }  // Azul
                    ].map((opcion) => {
                        const isActive = filters.estadosSeleccionados?.includes(opcion.id);
                        return (
                            <button
                                key={opcion.id}
                                type="button"
                                className={`toggle-btn ${isActive ? 'active' : ''}`}
                                onClick={() => {
                                    const actual = filters.estadosSeleccionados || [];
                                    const nuevos = actual.includes(opcion.id)
                                        ? actual.filter(i => i !== opcion.id)
                                        : [...actual, opcion.id];
                                    setFilters({ ...filters, estadosSeleccionados: nuevos });
                                }}
                                style={isActive ? { borderColor: opcion.color, color: opcion.color } : {}}
                            >
                                {opcion.label}
                            </button>
                        );
                    })}
                </div>
            </div>

            {/* Filtro por Tipo de Lugar */}
            <div className="filtro-grupo">
                <label className="filtro-label">Tipos de lugar</label>
                <div className="lista-tipos-scroll">
                    {Object.entries(opcionesTipo).map(([grupo, opciones]) => (
                        <div key={grupo} className="grupo-categoria">
                            <span className="titulo-categoria">{grupo}</span>
                            {opciones.map(opt => (
                                <label key={opt.id} className="checkbox-item">
                                    <input
                                        type="checkbox"
                                        checked={filters.tiposSeleccionados.includes(opt.id)}
                                        onChange={() => {
                                            const actual = filters.tiposSeleccionados;
                                            const nuevos = actual.includes(opt.id)
                                                ? actual.filter(i => i !== opt.id)
                                                : [...actual, opt.id];
                                            setFilters({ ...filters, tiposSeleccionados: nuevos });
                                        }}
                                    />
                                    <span>{opt.label}</span>
                                </label>
                            ))}
                        </div>
                    ))}
                </div>
            </div>

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