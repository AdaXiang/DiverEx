import { React, useEffect, useState, useContext } from "react";
import './Filtros.css';
import { AuthContext } from "../../context/AuthContext";

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

const detalleToTipo = {
    "PU": "Parque",
    "PN": "Parque",
    "PI": "Parque",
    "JA": "Parque",
    "AN": "Parque",
    "ZR": "Parque",

    "LO": "Lonja",
    "ME": "Lonja",
    "FE": "Lonja"
};

export default function Filtros({ filters, setFilters, userLocation, modoFiltro, setModoFiltro, recommendationFilters, setRecommendationFilters }) {

    const { user } = useContext(AuthContext);
    //recomendaciones estandar, solo por gusto
    //control visual
    const soloLonjas = recommendationFilters.tipo.length === 1 && recommendationFilters.tipo.includes("Lonja");

    return (
        <div className="filtros-panel-estatico">
            {user && ( <div className="menu">
                <button className={modoFiltro ? "active" : ""}  onClick={() => setModoFiltro(true)} > 🌍 Filtros </button>
                <button className={!modoFiltro ? "active" : ""} onClick={() => setModoFiltro(false)} > ✨ Recomendaciones </button>
            </div> )}
            {!user && <h2>Filtros</h2> }

            {/* MODO FILTRO GROGRAFICO */}
            { modoFiltro ? (
                <>
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
                            <p className="mensaje-informativo"> Coordenadas: {userLocation.lat.toFixed(4)}, {userLocation.lng.toFixed(4)} </p>
                        ) : (
                            <span className="mensaje-error">Calculando tu ubicación...</span>
                        )}
                    </div>
                </>
            ):(
                <>
                {/* MODO FILTRO RECOMENDACIONES */}
                {/* Accesibilidad */}
                    <label className="filtro-item">
                        <input
                            type="checkbox"
                            checked={recommendationFilters.accesible}
                            onChange={(e) =>
                                setRecommendationFilters({
                                    ...recommendationFilters,
                                    accesible: e.target.checked
                                })
                            }
                        />
                        Accesible silla de ruedas
                    </label>

                    {/* Juegos */}
                    {/*<label className="filtro-item">
                        <input
                            type="checkbox"
                            checked={recommendationFilters.juegos}
                            onChange={(e) =>
                                setRecommendationFilters({
                                    ...recommendationFilters,
                                    juegos: e.target.checked
                                })
                            }
                        />
                        Zonas infantiles
                    </label>*/}

                    {/* Comedor */}
                    {/* <label className={`filtro-item ${soloLonjas ? 'disabled' : ''}`} >
                        <input type="checkbox"  disabled={soloLonjas} checked={ !soloLonjas && recommendationFilters.comedor}
                            onChange={(e) => {
                                if (soloLonjas) return;

                                setRecommendationFilters({
                                    ...recommendationFilters,
                                    comedor: e.target.checked
                                });
                            }}
                        />
                        Comedor
                    </label>*/}

                    {/* Agua */}
                    {/*<label className={`filtro-item ${soloLonjas ? 'disabled' : ''}`} >
                        <input type="checkbox"  disabled={soloLonjas} checked={ !soloLonjas && recommendationFilters.agua }
                            onChange={(e) => {
                                if (soloLonjas) return;

                                setRecommendationFilters({
                                    ...recommendationFilters,
                                    agua: e.target.checked 
                                });
                            }}
                        />
                        Agua
                    </label>*/}

                    {/* Electricidad */}
                    {/*<label className={`filtro-item ${soloLonjas ? 'disabled' : ''}`} >
                        <input type="checkbox"  disabled={soloLonjas} checked={ !soloLonjas && recommendationFilters.electricidad }
                            onChange={(e) => {
                                if (soloLonjas) return;

                                setRecommendationFilters({
                                    ...recommendationFilters,
                                    electricidad: e.target.checked 
                                });
                            }}
                        />
                        Electricidad
                    </label> */}

                    {/* Estado */}
                    <div className="filtro-grupo">

                        <label className="filtro-label">
                            Estado de conservación
                        </label>

                        <div className="toggle-container">

                            {[
                                { id: 'B', label: 'B', color: '#2ecc71' },
                                { id: 'R', label: 'R', color: '#f1c40f' },
                                { id: 'M', label: 'M', color: '#e74c3c' },
                                { id: 'E', label: 'E', color: '#3498db' }
                            ].map((opcion) => {

                                const isActive =
                                    recommendationFilters.estado.includes(opcion.id);

                                return (
                                    <button
                                        key={opcion.id}
                                        type="button"
                                        className={`toggle-btn ${isActive ? 'active' : ''}`}

                                        onClick={() => {

                                            const actual =
                                                recommendationFilters.estado;

                                            const nuevos =
                                                actual.includes(opcion.id)
                                                    ? actual.filter(i => i !== opcion.id)
                                                    : [...actual, opcion.id];

                                            setRecommendationFilters({
                                                ...recommendationFilters,
                                                estado: nuevos
                                            });
                                        }}

                                        style={
                                            isActive
                                                ? {
                                                    borderColor: opcion.color,
                                                    color: opcion.color
                                                }
                                                : {}
                                        }
                                    >
                                        {opcion.label}
                                    </button>
                                );
                            })}

                        </div>
                    </div>

                    {/* Tipo detalle */}
                    <div className="filtro-grupo">

                        <label className="filtro-label">
                            Categorías
                        </label>

                        <div className="lista-tipos-scroll">

                            {Object.entries(opcionesTipo).map(([grupo, opciones]) => (

                                <div
                                    key={grupo}
                                    className="grupo-categoria"
                                >

                                    <span className="titulo-categoria">
                                        {grupo}
                                    </span>

                                    {opciones.map(opt => (

                                        <label
                                            key={opt.id}
                                            className="checkbox-item"
                                        >

                                            <input
                                                type="checkbox"

                                                checked={
                                                    recommendationFilters
                                                        .tipo_detalle
                                                        .includes(opt.id)
                                                }

                                                onChange={() => {
                                                    const actual = recommendationFilters.tipo_detalle;
                                                    const nuevos = actual.includes(opt.id) ? actual.filter(i => i !== opt.id) : [...actual, opt.id];

                                                    // detectar tipos automáticamente
                                                    const tiposDetectados = [
                                                        ...new Set(
                                                            nuevos.map(id => detalleToTipo[id])
                                                        )
                                                    ];

                                                    const soloLonjas = tiposDetectados.length === 1 && tiposDetectados.includes("Lonja");

                                                    setRecommendationFilters({
                                                        ...recommendationFilters,
                                                        tipo_detalle: nuevos,
                                                        tipo: tiposDetectados,
                                                        agua: soloLonjas ? null : (recommendationFilters.agua ?? false),
                                                        electricidad: soloLonjas ? null : (recommendationFilters.electricidad ?? false),
                                                        comedor: soloLonjas ? null : (recommendationFilters.comedor ?? false)
                                                    });
                                                }}
                                            />

                                            <span>
                                                {opt.label}
                                            </span>

                                        </label>

                                    ))}

                                </div>

                            ))}

                        </div>
                    </div>

                    {/* Valoración */}
                    <div className="filtro-grupo">

                        <label className="filtro-label">
                            Valoración media
                        </label>

                        <div className="select-rating-container">

                            {/* mínimo */}
                            <select
                                className="rating-select"

                                value={recommendationFilters.media_min ?? 1}

                                onChange={(e) => {

                                    const value =
                                        Number(e.target.value);

                                    setRecommendationFilters({
                                        ...recommendationFilters,
                                        media_min: value,
                                        media_max:
                                            value >
                                            (recommendationFilters.media_max ?? 5)
                                                ? value
                                                : recommendationFilters.media_max
                                    });
                                }}
                            >

                                <option value={1}>1⭐</option>
                                <option value={2}>2⭐</option>
                                <option value={3}>3⭐</option>
                                <option value={4}>4⭐</option>
                                <option value={5}>5⭐</option>

                            </select>

                            <span className="rating-separator">
                                —
                            </span>

                            {/* máximo */}
                            <select
                                className="rating-select"

                                value={recommendationFilters.media_max ?? 5}

                                onChange={(e) =>
                                    setRecommendationFilters({
                                        ...recommendationFilters,
                                        media_max: Number(e.target.value)
                                    })
                                }
                            >

                                {[1, 2, 3, 4, 5].map((n) => (

                                    <option
                                        key={n}
                                        value={n}
                                        disabled={
                                            n <
                                            (recommendationFilters.media_min ?? 1)
                                        }
                                    >
                                        {n}⭐
                                    </option>

                                ))}

                            </select>

                        </div>

                    </div>
                </>
            )}
        </div>
    );
}