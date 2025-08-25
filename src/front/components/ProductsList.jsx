// src/front/components/ProductsList.jsx
import React, { useEffect, useState } from 'react';
import { getProducts, addToCart } from "../lib/api.js";
import { Link } from "react-router-dom";

export default function ProductsList() {
  const [products, setProducts] = useState([]);
  const [addingId, setAddingId] = useState(null);
  const [msg, setMsg] = useState("");

  const BASE = import.meta.env.VITE_BACKEND_URL;
  const PLACEHOLDER = `${BASE}/static/images/placeholder.jpg`;

  // Resolver URL final de imagen (por si viene relativa)
  const imgSrc = (p) => {
    if (!p?.image_url) return PLACEHOLDER;
    if (p.image_url.startsWith('http')) return p.image_url;
    const needsSlash = p.image_url.startsWith('/') ? '' : '/';
    return `${BASE}${needsSlash}${p.image_url}`;
  };

  useEffect(() => {
    getProducts()
      .then(setProducts)
      .catch(err => console.error('Error fetching products:', err));
  }, []);

  async function handleAdd(p) {
    try {
      setAddingId(p.id);
      await addToCart(p.id, 1);
      setMsg(`Añadido: ${p.name} ✅`);
      window.dispatchEvent(new Event("cart:refresh")); 
      setTimeout(() => setMsg(""), 1500);
    } catch (e) {
      console.error(e);
      setMsg(
        e.message?.includes("401")
          ? "Debes iniciar sesión para agregar al carrito."
          : (e.message || "Error al agregar.")
      );
      setTimeout(() => setMsg(""), 2500);
    } finally {
      setAddingId(null);
    }
  }

  return (
    <div>
      <h2>Catálogo de Jabones</h2>
      {msg && (
        <div style={{ margin:'8px 0', padding:'8px', background:'#eef', borderRadius:8 }}>
          {msg}
        </div>
      )}

      <ul style={{
        display:'grid',
        gridTemplateColumns:'repeat(auto-fill, minmax(220px, 1fr))',
        gap:16, listStyle:'none', padding:0, margin:0
      }}>
        {products.map(product => (
          <li
            key={product.id}
            style={{
              border:'1px solid #eee',
              borderRadius:16,
              padding:12,
              display:'flex',                // <-- hace la tarjeta en columna
              flexDirection:'column',        //     para poder “pegar” el botón abajo
              minHeight: 380                
            }}
          >
            <Link to={`/product/${product.id}`} style={{ textDecoration: 'none', color: 'inherit' }}>
              <img
                src={imgSrc(product)}
                alt={product.name}
                loading="lazy"
                decoding="async"
                style={{ width:'100%', aspectRatio:'1/1', objectFit:'cover', borderRadius:12, display:'block' }}
                onError={(e) => { e.currentTarget.src = PLACEHOLDER; }}
              />
              <h3 style={{ margin:'12px 0 6px', minHeight: 44 /* ~2 líneas */ }}>
                {product.name}
              </h3>
            </Link>

            <div style={{ fontWeight:700, marginBottom:8 }}>€{Number(product.price).toFixed(2)}</div>

            <p
              style={{
                fontSize:14,
                color:'#555',
                minHeight: 60,      // <-- bloquea altura mínima de descripción
                marginBottom: 12
              }}
            >
              {product.description}
            </p>

            <button
              onClick={() => handleAdd(product)}
              disabled={addingId === product.id}
              style={{
                width:'100%',
                padding:'10px 12px',
                borderRadius:12,
                border:'none',
                background: addingId === product.id ? '#aaa' : '#222',
                color:'#fff',
                cursor: addingId === product.id ? 'wait' : 'pointer',
                marginTop: 'auto'   // <-- empuja el botón al fondo de la tarjeta
              }}
              aria-label="Agregar al carrito"
              title="Agregar al carrito"
            >
              {addingId === product.id ? 'Añadiendo…' : '🛒'}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
