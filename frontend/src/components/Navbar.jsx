import { useEffect, useState } from "react";
import { NavLink, useNavigate } from "react-router-dom";

import api from "../services/api";


function Navbar() {
  const navigate = useNavigate();

  const [user, setUser] = useState(null);


  useEffect(() => {
    const loadUser = async () => {
      const token = localStorage.getItem(
        "careermatch_token"
      );

      if (!token) {
        return;
      }

      try {
        const response = await api.get(
          "/users/me"
        );

        setUser(response.data);
      } catch (error) {
        console.error(
          "Unable to load current user:",
          error
        );
      }
    };

    loadUser();
  }, []);


  const logout = () => {
    localStorage.removeItem(
      "careermatch_token"
    );

    navigate("/login");
  };


  const navClass = ({ isActive }) =>
    `nav-link${isActive ? " active" : ""}`;


  const isAdmin = user?.role === "admin";


  return (
    <nav className="navbar">

      <div className="logo">
        CareerMatch AI
      </div>


      <div className="nav-links">

        <NavLink
          to="/dashboard"
          className={navClass}
        >
          Dashboard
        </NavLink>


        <NavLink
          to="/resume"
          className={navClass}
        >
          Resume
        </NavLink>


        <NavLink
          to="/jobs"
          className={navClass}
        >
          Jobs
        </NavLink>


        <NavLink
          to="/recommendations"
          className={navClass}
        >
          Recommendations
        </NavLink>


        <NavLink
          to="/matches"
          className={navClass}
        >
          Matches
        </NavLink>


        {!isAdmin && (
          <NavLink
            to="/applications"
            className={navClass}
          >
            Applications
          </NavLink>
        )}


        {isAdmin && (
          <NavLink
            to="/admin/applications"
            className={navClass}
          >
            Admin Applications
          </NavLink>
        )}


        {isAdmin && (
          <span
            style={{
              display: "inline-flex",
              alignItems: "center",
              padding: "6px 10px",
              borderRadius: "6px",
              background: "#eee",
              fontSize: "13px",
              fontWeight: 600,
            }}
          >
            Admin
          </span>
        )}


        <button
          className="logout-btn"
          onClick={logout}
        >
          Logout
        </button>

      </div>

    </nav>
  );
}


export default Navbar;
