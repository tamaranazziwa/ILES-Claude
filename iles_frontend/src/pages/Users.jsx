import {useState, useEffect} from "react";
import API from "../services/api";
import Layout from "../components/Layout";

function Users() {
    const[users,setUsers] = useState([]);
    useEffect(() => {
        const fetchUsers = async () => {
            try {
                const res = await API.get("/users"); // adjust endpoint
                setUsers(res.data);
            } catch (err) {
                console.log(err);
            }
        };
        fetchUsers();
    }, []); 
    
    return (
        <Layout>
            <h1>Users page</h1>
            <table border="1" cellPadding="10">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Username</th>
                    <th>Role</th>
                  </tr>
                </thead>

                 <tbody>
                  {users.map((user) => (
                    <tr key={user.id}>
                      <td>{user.id}</td>
                      <td>{user.username}</td>
                      <td>{user.role}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
        </Layout>
    );
}

export default Users;
