import { NavLink } from "react-router-dom";

function Layout({ children }) {
  const linkStyle = {
    display: "block",
    padding: "12px 16px",
    textDecoration: "none",
    color: "white",
  };

  const activeStyle = {
    backgroundColor: "#334155",
    fontWeight: "bold",
  };

  const sidebarStyle = {
    width: "220px",
    background: "#1e293b",
    color: "white",
    minHeight: "100vh",
  };

  return (
    <div style={{ display: "flex", minHeight: "100vh" }}>
      <div style={sidebarStyle}>
        <NavLink
          to="/"
          style={({ isActive }) =>
            isActive ? { ...linkStyle, ...activeStyle } : linkStyle
          }
        >
          Home
        </NavLink>

        <NavLink
          to="/users"
          style={({ isActive }) =>
            isActive ? { ...linkStyle, ...activeStyle } : linkStyle
          }
        >
          Users
        </NavLink>

        <NavLink
          to="/settings"
          style={({ isActive }) =>
            isActive ? { ...linkStyle, ...activeStyle } : linkStyle
          }
        >
          Settings
        </NavLink>

        <NavLink
          to="/logs"
          style={({ isActive }) =>
            isActive ? { ...linkStyle, ...activeStyle } : linkStyle
          }
        >
          Logs
        </NavLink>
      </div>

      <div style={{ padding: "20px", flex: 1 }}>
        {children}
      </div>
    </div>
  );
}

export default Layout;