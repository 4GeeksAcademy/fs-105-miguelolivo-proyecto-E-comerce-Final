// src/front/lib/api.js
const BASE = import.meta.env.VITE_BACKEND_URL;

export async function getProducts() {
  const res = await fetch(`${BASE}/api/products`);
  if (!res.ok) throw new Error("Error al cargar productos");
  return res.json();
}

export async function addToCart(productId, qty = 1) {
  const token = localStorage.getItem("jwt_token");
  if (!token) throw new Error("401: No autorizado");

  const res = await fetch(`${BASE}/api/cart`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ product_id: productId, quantity: qty }),
  });

  if (!res.ok) {
    const data = await res.json();
    throw new Error(data.error || `HTTP ${res.status}`);
  }

  return res.json(); 
}
