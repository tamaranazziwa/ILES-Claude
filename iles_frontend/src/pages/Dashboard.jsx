import { useEffect, useState } from "react";
import API from "../services/api";
import Layout from "../components/Layout";

function Dashboard() {
  const [user, setUser] = useState(null);
  const [stats, setStats] = useState(null);

  const cardStyle = {
    padding: "20px",
    background: "#1e293b",
    color: "white",
    borderRadius: "8px",
    width: "150px", 
  };

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const res = await API.get("/user"); // adjust endpoint
        setUser(res.data);
      } catch (err) {
        console.log( "User error:", err);
      }
    };

    const fetchStats = async () => {
      try {
        const res = await API.get("/stats"); // adjust endpoint
        setStats(res.data);
      } catch (err) {
        console.log( "Stats error:", err);
      }
    };
    
    fetchUser();
    fetchStats();
  }, []);

  return (
    <Layout>
      <h1>Dashboard</h1>
      {user ? (
        <p>Welcome, {user.username}</p>
      ) : (
        <p>Loading...</p>
      )}

      {stats ? (
        <div>
          <h2>Statistics</h2>
          <p>Total Users: {stats.totalUsers}</p>
          <p>Total Products: {stats.totalProducts}</p>
          <p>Active Sessions: {stats.activeSessions}</p>
          <p>Total Orders: {stats.totalOrders}</p>
        </div>
      ) : (
        <p>Loading stats...</p>
      )}

      <div style={{ display: "flex", gap: "20px" }}>
        <div style={cardStyle}>
          <h3>Users</h3>
          <p>{stats?.users || 0}</p>
        </div>

        <div style={cardStyle}>
          <h3>Evaluations</h3>
          <p>{stats?.evaluations || 0}</p>
        </div>
        <div style={cardStyle}>
          <h3>Active</h3>
          <p>{stats?.active || 0}</p>
        </div>
      </div>
    </Layout>
  );
}
    

      

export default Dashboard;