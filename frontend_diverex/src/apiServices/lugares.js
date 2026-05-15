import apiC from "./clientCouch";

export const getLugares = async () => {
    try {
        const res = await apiC.get("/lugares");
        return res.data;
    } catch (err) {
        console.error("Error al obtener lugares:", err);
        throw err;
    }
};

export const getLugaresFiltrados = async (filters, ids_recomendaciones) => {
    try {
        // Usamos URLSearchParams para asegurar compatibilidad total con FastAPI
        const params = new URLSearchParams();

        console.log("Filtros enviados al API:", filters, "IDs de recomendaciones:", ids_recomendaciones);

        // booleanos
        if (filters.sillaRuedas) params.append('acceso_silla_ruedas', 'true');
        if (filters.zonaInfantil) params.append('zona_infantil', 'true');
        if (filters.comedor) params.append('comedor', 'true');

        // geo
        if (filters.lat && filters.lon) {
            params.append('lat', filters.lat);
            params.append('lon', filters.lon);
            params.append('distancia_max', filters.distanciaMax || 1000);
        }

        // arrays (Axios no usará corchetes '[]', que es lo que FastAPI espera)
        if (filters.estadosSeleccionados?.length) {
            filters.estadosSeleccionados.forEach(e => params.append('estado', e));
        }

        if (filters.tiposSeleccionados?.length) {
            filters.tiposSeleccionados.forEach(t => params.append('tipo_lugar', t));
        }

        // Lista de recomendaciones
        if (ids_recomendaciones && ids_recomendaciones.length > 0) {
            // FastAPI leerá esto como una lista: ?recomendacion=id1&recomendacion=id2
            ids_recomendaciones.forEach(id => params.append('recomendacion', id));
        }

        // texto
        if (filters.busquedaTexto) {
            const texto = filters.busquedaTexto;

            if (texto.includes(',')) {
                const [nombre, municipio] = texto.split(',').map(t => t.trim());
                if (nombre) params.append('nombre', nombre);
                if (municipio) params.append('municipio', municipio);
            } else {
                params.append('nombre', texto.trim());
            }
        }

        const res = await apiC.get("/lugares/filtrar", { params });

        return res.data;

    } catch (err) {
        console.error("Error:", err);
        if (err.response) {
            console.error("Status:", err.response.status);
            console.error("Body:", err.response.data);
        }
        throw err;
    }
};

export const getLugar = async (id) => {
    try {
        const res = await apiC.get(`/lugar/${id}`);
        return res.data;
    } catch (err) {
        console.error("Error al obtener lugar:", err);
        throw err;
    }
};