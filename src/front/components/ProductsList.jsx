import React, { useEffect, useState } from 'react';

export default function ProductsList() {
  const [products, setProducts] = useState([]);
  const BASE = import.meta.env.VITE_BACKEND_URL; // tu backend público
  const PLACEHOLDER = `${BASE}/static/images/placeholder.jpg`;

  // Función para resolver la URL final de la imagen
  const imgSrc = (p) => {
    if (!p?.image_url) return PLACEHOLDER;
    if (p.image_url.startsWith('http')) return p.image_url;
    const needsSlash = p.image_url.startsWith('/') ? '' : '/';
    return `${BASE}${needsSlash}${p.image_url}`;
  };

  useEffect(() => {
    fetch(`${BASE}/api/products?limit=10`)
      .then(res => res.json())
      .then(data => setProducts(data))
      .catch(err => console.error('Error fetching products:', err));
  }, []);

  return (
    <div>
      <h2>Catálogo de Jabones</h2>
      <ul>
        {products.map(product => (
          <li key={product.id}>
            <h3>{product.name} - ${product.price}</h3>
            <img
              src={imgSrc(product)}
              alt={product.name}
              width="150"
              onError={(e) => { e.currentTarget.src = PLACEHOLDER; }}
            />
            <p>{product.description}</p>
            <p><strong>Aroma:</strong> {product.aroma}</p>
            <p><em>{product.ritual}</em></p>
          </li>
        ))}
      </ul>
    </div>
  );
}
