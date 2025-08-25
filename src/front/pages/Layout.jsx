import React from "react";
import Navbar from "../components/Navbar.jsx";
import { Outlet } from "react-router-dom";

export default function Layout() {
  return (
    <>
      <Navbar />
      <main style={{ padding: 16 }}>
        <Outlet />
      </main>
    </>
  );
}
