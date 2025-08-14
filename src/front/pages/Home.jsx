import React, { useEffect, useState } from 'react';
import './Home.css';

export default function Home() {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    console.log('Backend URL:', import.meta.env.VITE_BACKEND_URL);
    fetch(`${import.meta.env.VITE_BACKEND_URL}/api/products`)
      .then(res => res.json())
      .then(data => setProducts(data))
      .catch(err => console.error('Error fetching products:', err));
  }, []);

  return (
    <div className="container">
      <h1>E-commerce de Jabones</h1>
      <h2>Catálogo de Jabones</h2>
      <ul className="product-list">
        {products.length === 0 && <li>Cargando productos...</li>}
        {products.map(product => (
          <li key={product.id} className="product-item">
            <h3>{product.name} - ${product.price.toFixed(2)}</h3>
            {product.image_url && <img src={product.image_url} alt={product.name} className="product-image" />}
            <p>{product.description}</p>
            <p><strong>Aroma:</strong> {product.aroma}</p>
            <p><em>{product.ritual}</em></p>
          </li>
        ))}
      </ul>
    </div>
  );
}
