import React, { useEffect, useState } from 'react';


export default function ProductsList() {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    fetch(`${import.meta.env.VITE_BACKEND_URL}/api/products?limit=10`)
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
            <img src={product.image_url} alt={product.name} width="150" />
            <p>{product.description}</p>
            <p><strong>Aroma:</strong> {product.aroma}</p>
            <p><em>{product.ritual}</em></p>
          </li>
        ))}
      </ul>
    </div>
  );
}
