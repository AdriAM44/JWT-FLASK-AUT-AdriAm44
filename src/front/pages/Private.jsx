import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export const Private = () => {
    const [message, setMessage] = useState("");
    const navigate = useNavigate();

    useEffect(() => {
        const token = sessionStorage.getItem("token");
        if (!token) {
            navigate("/login");
            return;
        }

        fetch(import.meta.env.VITE_BACKEND_URL + "/api/private", {
            headers: {
                "Authorization": "Bearer " + token
            }
        })
        .then(res => {
            if (!res.ok) throw new Error("No autorizado");
            return res.json();
        })
        .then(data => setMessage(data.logged_in_as))
        .catch(() => {
            sessionStorage.removeItem("token");
            navigate("/login");
        });
    }, [navigate]);

    return (
        <div className="container mt-5 text-center">
            <h2>Página Privada</h2>
            {message ? (
                <div className="alert alert-info mt-3">
                    Bienvenido, <strong>{message}</strong>. Tienes acceso autorizado.
                </div>
            ) : (
                <p>Cargando información protegida...</p>
            )}
        </div>
    );
};