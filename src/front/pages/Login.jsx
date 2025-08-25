import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage("");

    try {
      const res = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
      });
      const data = await res.json();

      if (res.ok) {
        localStorage.setItem("jwt_token", data.access_token);
        setMessage("✅ Sesión iniciada correctamente");
        // refrescar contador del carrito en Navbar (opcional)
        window.dispatchEvent(new Event("cart:refresh"));
        // redirigir al catálogo
        navigate("/");
      } else {
        setMessage(`❌ Error: ${data.error || "Credenciales inválidas"}`);
      }
    } catch (err) {
      setMessage("❌ Error de red/servidor");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="signup-container">
      <h2>Iniciar sesión</h2>
      <form className="signup-form" onSubmit={handleLogin}>
        <input
          type="email"
          placeholder="Correo electrónico"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          disabled={loading}
        />
        <input
          type="password"
          placeholder="Contraseña"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          disabled={loading}
        />
        <button type="submit" disabled={loading}>
          {loading ? "Entrando..." : "Entrar"}
        </button>
      </form>
      {message && <p className="signup-message">{message}</p>}
    </div>
  );
}
