// src/front/components/Navbar.jsx
import React, { useEffect, useState } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";

const BRAND = "SUDS";

export default function Navbar() {
  const navigate = useNavigate();
  const location = useLocation();
  const [cartCount, setCartCount] = useState(0);
  const isLoggedIn = !!localStorage.getItem("jwt_token");

  useEffect(() => {
    if (!isLoggedIn) { setCartCount(0); return; }
    const token = localStorage.getItem("jwt_token");
    fetch(`${import.meta.env.VITE_BACKEND_URL}/api/cart`, {
      headers: { Authorization: `Bearer ${token}` }
    })
      .then(r => (r.ok ? r.json() : []))
      .then(items => {
        const total = Array.isArray(items) ? items.reduce((a, it) => a + (it.quantity || 0), 0) : 0;
        setCartCount(total);
      })
      .catch(() => {});
  }, [isLoggedIn, location.pathname]);

  useEffect(() => {
    const refresh = () => {
      const token = localStorage.getItem("jwt_token");
      if (!token) return setCartCount(0);
      fetch(`${import.meta.env.VITE_BACKEND_URL}/api/cart`, {
        headers: { Authorization: `Bearer ${token}` }
      })
        .then(r => (r.ok ? r.json() : []))
        .then(items => {
          const total = Array.isArray(items) ? items.reduce((a, it) => a + (it.quantity || 0), 0) : 0;
          setCartCount(total);
        })
        .catch(() => {});
    };
    window.addEventListener("cart:refresh", refresh);
    return () => window.removeEventListener("cart:refresh", refresh);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("jwt_token");
    setCartCount(0);
    navigate("/login");
  };

  return (
    <nav style={{ padding: "10px", background: "#eee", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
      {/* Marca a la izquierda (ahora hace de Home) */}
      <Link to="/" style={{ fontWeight: "bold", color: "#000", textDecoration: "none" }}>
        {BRAND}
      </Link>

      {/* Pestañas a la derecha (sin Home) */}
      <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
        {!isLoggedIn && (
          <>
            <Link to="/signup">Signup</Link>
            <Link to="/login">Login</Link>
          </>
        )}

        {isLoggedIn && (
          <>

            <Link to="/cart" style={{ position: "relative", paddingRight: "6px" }}>
              🛒
              {cartCount > 0 && (
                <span
                  style={{
                    position: "absolute",
                    top: "-6px",
                    right: "-12px",
                    background: "#333",
                    color: "#fff",
                    fontSize: "11px",
                    lineHeight: 1,
                    padding: "4px 6px",
                    borderRadius: "999px",
                    minWidth: "18px",
                    textAlign: "center",
                    border: "2px solid #eee"
                  }}
                >
                  {cartCount}
                </span>
              )}
            </Link>
            
            <button
              onClick={handleLogout}
              style={{ background: "transparent", border: "none", cursor: "pointer", color: "green" }}
            >
              Logout
            </button>
          </>
        )}
      </div>
    </nav>
  );
}
