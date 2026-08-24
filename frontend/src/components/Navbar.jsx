import { NavLink, useNavigate } from "react-router-dom";

function Navbar() {
  const navigate = useNavigate();

  const logout = () => {
    localStorage.removeItem("careermatch_token");
    navigate("/login");
  };

  const navClass = ({ isActive }) =>
    `nav-link${isActive ? " active" : ""}`;

  return (
    <nav className="navbar">
      <div className="logo">CareerMatch AI</div>

      <div className="nav-links">
        <NavLink to="/dashboard" className={navClass}>
          Dashboard
        </NavLink>

        <NavLink to="/resume" className={navClass}>
          Resume
        </NavLink>

        <NavLink to="/jobs" className={navClass}>
          Jobs
        </NavLink>

        <NavLink
          to="/recommendations"
          className={navClass}
        >
          Recommendations
        </NavLink>

        <NavLink to="/matches" className={navClass}>
          Matches
        </NavLink>

        <button className="logout-btn" onClick={logout}>
          Logout
        </button>
      </div>
    </nav>
  );
}

export default Navbar;
