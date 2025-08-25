import React, { useState, useEffect } from "react";

export default function Signup() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [showBubbles, setShowBubbles] = useState(false);

  // Oculta las burbujas automáticamente 
  useEffect(() => {
    if (!showBubbles) return;
    const t = setTimeout(() => setShowBubbles(false), 2200);
    return () => clearTimeout(t);
  }, [showBubbles]);

  const handleSignup = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage("");
    try {
      const res = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/auth/signup`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
      });
      const data = await res.json();
      if (res.ok) {
        localStorage.setItem("jwt_token", data.access_token);
        setMessage("✅ Usuario creado con éxito");
        setShowBubbles(true);              // animación
      } else {
        setMessage(`❌ Error: ${data.error || "No se pudo registrar"}`);
      }
    } catch (err) {
      setMessage("❌ Error en el servidor");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="signup-container">
      <h2>Registro</h2>

      {/* contenedor de burbujas */}
      {showBubbles && (
        <div className="bubbles" aria-hidden="true">
          <span className="bubble b1" />
          <span className="bubble b2" />
          <span className="bubble b3" />
          <span className="bubble b4" />
          <span className="bubble b5" />
        </div>
      )}

      <form onSubmit={handleSignup} className="signup-form">
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
          {loading ? "Registrando..." : "Registrarse"}
        </button>
      </form>
      {message && <p className="signup-message">{message}</p>}
    </div>
  );
}
