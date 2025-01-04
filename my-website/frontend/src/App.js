import { NavLink, Routes, Route, Navigate} from 'react-router-dom';
import About from './pages/About';
import Projects from './pages/Projects';
import Experience from './pages/Experience';
import Other from './pages/Other';
import "./App.css";


export default function App() {
  return (
    <div>
      <nav className="navbar navbar-expand-lg navbar-light bg-light border-bottom border-2">
        <div className="container-fluid">
        <span className="navbar-brand">
          Christopher Apton
        </span>
          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon" />
          </button>

          <div className="collapse navbar-collapse" id="navbarSupportedContent">
            <ul className="navbar-nav mx-auto border-start border-end border-2 px-0">
            <li className="nav-item border-end border-2 me-0">
  <NavLink
    className={({ isActive }) =>
      isActive ? 'nav-link fs-4 active' : 'nav-link fs-4'
    }
    to="/about"
  >
    About
  </NavLink>
</li>
<li className="nav-item border-end border-2 me-0">
  <NavLink
    className={({ isActive }) =>
      isActive ? 'nav-link fs-4 active' : 'nav-link fs-4'
    }
    to="/projects"
  >
    Projects
  </NavLink>
</li>
<li className="nav-item border-end border-2 me-0">
  <NavLink
    className={({ isActive }) =>
      isActive ? 'nav-link fs-4 active' : 'nav-link fs-4'
    }
    to="/experience"
  >
    Experience
  </NavLink>
</li>
<li className="nav-item border-end border-2 me-0">
  <NavLink
    className={({ isActive }) =>
      isActive ? 'nav-link fs-4 active' : 'nav-link fs-4'
    }
    to="/other"
  >
    Other
  </NavLink>
</li>

            </ul>
          </div>
        </div>
      </nav>

      <div className="container mt-5">
        <Routes>
          <Route path="/" element={<Navigate to="/about" replace />} />
          <Route path="/about" element={<About />} />
          <Route path="/projects" element={<Projects />} />
          <Route path="/experience" element={<Experience />} />
          <Route path="/other" element={<Other />} />
        </Routes>
      </div>
    </div>
  );
}

