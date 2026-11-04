import { NavLink, Route, Routes } from "react-router-dom";

import { HealthBadge } from "./components/HealthBadge";
import { About } from "./pages/About";
import { Rooms } from "./pages/Rooms";

/**
 * Routes live here; the router itself is provided by main.tsx (HashRouter,
 * so deep links work on static hosting) or by tests (MemoryRouter).
 */
export function App() {
  return (
    <main>
      <header>
        <h1>EscapeQueue</h1>
        <HealthBadge />
      </header>
      <nav>
        <NavLink to="/" end>
          Rooms
        </NavLink>
        <NavLink to="/about">About</NavLink>
      </nav>

      <Routes>
        <Route path="/" element={<Rooms />} />
        <Route path="/about" element={<About />} />
        <Route path="*" element={<p>Page not found.</p>} />
      </Routes>
    </main>
  );
}
