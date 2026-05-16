// components/loading/Loading.jsx

import { useEffect, useState } from "react";
import "./Loading.css";

export default function Loading({
    text = "Cargando...",
    visible = true
}) {

    const [show, setShow] =
        useState(visible);

    useEffect(() => {

        setShow(visible);

    }, [visible]);

    if (!show) return null;

    return (
        <div className="loading-overlay">

            <div className="loading-box">

                <div className="loading-spinner"></div>

                <h2 className="loading-title">
                    {text}
                </h2>

                <p className="loading-subtitle">
                    Espera un momento...
                </p>

            </div>

        </div>
    );
}