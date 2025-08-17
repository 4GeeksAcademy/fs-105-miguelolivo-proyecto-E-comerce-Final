import React, { useEffect, useMemo, useState } from 'react';

export default function ProductsList() {
  const [products, setProducts] = useState([]);

  
  const BASE = useMemo(() => {
    const envBase = import.meta.env.VITE_BACKEND_URL?.trim();
    if (envBase) return envBase;
    try {
      const here = new URL(window.location.href).origin; 
      if (here.includes('-3002')) return here.replace('-3002', '-3001');
      return here;
    } catch {
      return '';
    }
  }, []);

  const PLACEHOLDER = `${BASE}/static/images/placeholder.jpg`;

  // URL final de imagen
  const imgSrc = (p) => {
    const url = p?.image_url || '';
    if (!url) return PLACEHOLDER;
    if (url.startsWith('http')) return url; 
    const needsSlash = url.startsWith('/') ? '' : '/';
    return `${BASE}${needsSlash}${url}`;
  };

  useEffect(() => {
    console.log('✅ Backend BASE usado para imágenes y fetch:', BASE);
    fetch(`${BASE}/api/products?limit=10`)
      .then(res => res.json())
      .then(data => setProducts(data))
      .catch(err => console.error('Error fetching products:', err));
  }, [BASE]);

  return (
    <div>
      <h2>Catálogo de Jabones</h2>
      <ul>
        {products.map(product => {
          const src = imgSrc(product);
          return (
            <li key={product.id}>
              <h3>{product.name} - €{Number(product.price).toFixed(2)}</h3>
              <img
                src={src}
                alt={product.name}
                width="150"
                onError={(e) => { e.currentTarget.src = PLACEHOLDER; }}
              />
              <p>{product.description}</p>
              <p><strong>Aroma:</strong> {product.aroma}</p>
              <p><em>{product.ritual}</em></p>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
