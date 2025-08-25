// src/front/pages/ProductDetail.jsx
import React, { useEffect, useMemo, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

const FAVORITES_KEY = "favorites_ids";

function useFavorites() {
  const [ids, setIds] = useState(() => {
    try { return JSON.parse(localStorage.getItem(FAVORITES_KEY) || "[]"); }
    catch { return []; }
  });

  const isFav = (id) => ids.includes(id);
  const toggle = (id) => {
    setIds(prev => {
      const next = prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id];
      localStorage.setItem(FAVORITES_KEY, JSON.stringify(next));
      return next;
    });
  };

  return { ids, isFav, toggle };
}

export default function ProductDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [product, setProduct] = useState(null);
  const [cartItemId, setCartItemId] = useState(null);
  const [qty, setQty] = useState(1);
  const [status, setStatus] = useState("");

  const token = localStorage.getItem("jwt_token");
  const { isFav, toggle } = useFavorites();

  const BASE = import.meta.env.VITE_BACKEND_URL;
  const PLACEHOLDER = `${BASE}/static/images/placeholder.jpg`;
  const imgSrc = (p) => {
    if (!p?.image_url) return PLACEHOLDER;
    if (p.image_url.startsWith("http")) return p.image_url;
    const needsSlash = p.image_url.startsWith("/") ? "" : "/";
    return `${BASE}${needsSlash}${p.image_url}`;
  };

  // Cargar producto
  useEffect(() => {
    const load = async () => {
      try {
        const res = await fetch(`${BASE}/api/products/${id}`);
        const data = await res.json();
        if (res.ok) setProduct(data);
      } catch (e) {
        console.error(e);
      }
    };
    load();
  }, [id, BASE]);

  // Comprobar si ya está en el carrito (para mostrar "Eliminar")
  useEffect(() => {
    const loadCart = async () => {
      if (!token) { setCartItemId(null); return; }
      try {
        const res = await fetch(`${BASE}/api/cart`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        const items = await res.json();
        if (Array.isArray(items)) {
          const found = items.find(it => it.product?.id === Number(id));
          setCartItemId(found?.id || null);
        } else {
          setCartItemId(null);
        }
      } catch {
        setCartItemId(null);
      }
    };
    loadCart();
  }, [id, BASE, token]); // <-- aquí cerramos bien el useEffect

  // Textos (temporal hasta que tengas campos en BD)
  const uso = useMemo(
    () => product?.ritual || "Usar a diario con agua tibia. Enjuagar y secar con suavidad.",
    [product]
  );
  const beneficios = useMemo(
    () => `Aroma: ${product?.aroma || "suave"} • Limpieza y cuidado de la piel • Sensación agradable e hidratación.`,
    [product]
  );
  const advertencias = useMemo(
    () => "Evitar contacto con ojos. Mantener fuera del alcance de niños. Suspender uso ante irritación.",
    []
  );

  const addToCart = async () => {
    setStatus("");
    if (!token) { setStatus("🔒 Inicia sesión para añadir al carrito"); return; }
    try {
      const res = await fetch(`${BASE}/api/cart`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({ product_id: Number(id), quantity: Number(qty) || 1 })
      });
      const data = await res.json();
      if (res.ok) {
        setStatus("✅ Producto añadido al carrito");
        window.dispatchEvent(new Event("cart:refresh"));
        setCartItemId(data?.id || cartItemId);
      } else {
        setStatus(`❌ ${data.error || "No se pudo añadir"}`);
      }
    } catch {
      setStatus("❌ Error de red/servidor");
    }
  };

  const removeFromCart = async () => {
    setStatus("");
    if (!token || !cartItemId) return;
    try {
      const res = await fetch(`${BASE}/api/cart/item/${cartItemId}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` }
      });
      if (res.ok) {
        setStatus("🗑️ Eliminado del carrito");
        setCartItemId(null);
        window.dispatchEvent(new Event("cart:refresh"));
      } else {
        const data = await res.json();
        setStatus(`❌ ${data.error || "No se pudo eliminar"}`);
      }
    } catch {
      setStatus("❌ Error de red/servidor");
    }
  };

  if (!product) {
    return (
      <div className="signup-container">
        <p>Cargando producto...</p>
      </div>
    );
  }

  return (
    <div className="signup-container" style={{ gap: 16 }}>
      <div className="signup-form" style={{ width: 760, maxWidth: "90vw" }}>
        <div style={{ display: "grid", gridTemplateColumns: "300px 1fr", gap: 24 }}>
          <div>
            <img
              src={imgSrc(product)}
              alt={product.name}
              onError={(e) => { e.currentTarget.src = PLACEHOLDER; }}
              style={{ width: "100%", aspectRatio: "1 / 1", objectFit: "cover", borderRadius: 12 }}
            />
          </div>

          <div>
            <h2 style={{ marginTop: 0 }}>{product.name}</h2>
            <p style={{ marginTop: 8, color: "#555" }}>{product.description}</p>
            <p style={{ fontWeight: 600, margin: "12px 0" }}>€{Number(product.price).toFixed(2)}</p>

            <section>
              <h4 style={{ margin: "8px 0" }}>Uso</h4>
              <p>{uso}</p>
            </section>
            <section>
              <h4 style={{ margin: "8px 0" }}>Beneficios</h4>
              <p>{beneficios}</p>
            </section>
            <section>
              <h4 style={{ margin: "8px 0", color: "#a33" }}>Advertencias</h4>
              <p>{advertencias}</p>
            </section>

            <div style={{ display: "flex", gap: 8, marginTop: 12, alignItems: "center", flexWrap: "wrap" }}>
              {/* Favoritos (localStorage) */}
              <button
                onClick={() => toggle(product.id)}
                style={{
                  background: isFav(product.id) ? "#ffd54f" : "#eee",
                  border: "1px solid #ddd",
                  borderRadius: 8,
                  padding: "8px 12px",
                  cursor: "pointer"
                }}
              >
                {isFav(product.id) ? "★ En favoritos" : "☆ Añadir a favoritos"}
              </button>

              {/* Cantidad */}
              <input
                type="number"
                min={1}
                value={qty}
                onChange={(e) => setQty(e.target.value)}
                style={{ width: 70, padding: 8, borderRadius: 8, border: "1px solid #ddd" }}
              />

              {/* Carrito */}
              <button
                onClick={addToCart}
                style={{ background: "#333", color: "#fff", border: "none", borderRadius: 8, padding: "8px 12px", cursor: "pointer" }}
              >
                Añadir al carrito
              </button>

              {cartItemId && (
                <button
                  onClick={removeFromCart}
                  style={{ background: "transparent", color: "#c33", border: "1px solid #c33", borderRadius: 8, padding: "8px 12px", cursor: "pointer" }}
                >
                  Eliminar del carrito
                </button>
              )}

              <button
                onClick={() => navigate(-1)}
                style={{ marginLeft: "auto", background: "transparent", border: "1px solid #ddd", borderRadius: 8, padding: "8px 12px", cursor: "pointer" }}
              >
                ← Volver
              </button>
            </div>

            {status && <p className="signup-message" style={{ marginTop: 10 }}>{status}</p>}
          </div>
        </div>
      </div>
    </div>
  );
}
