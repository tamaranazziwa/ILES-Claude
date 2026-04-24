import {useState, useEffect } from 'react';
import axios from 'axios';
// This line imports the React library and the useState hook.
function App() {
  // memory boxes for username, and other stuff
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');//error message
  const [user, setUser] = useState(null); //no user logged in
  const [newLog, setNewLog] = useState({ week_number: '', activities: '', placement: '' });
  const [message, setMessage] = useState('');        // Success/error message when creating log
  // This function runs when the form is submitted.
  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      try {
        const payload = JSON.parse(atob(token.split('.')[1]));//get usernme from token
        setUser({ username: payload.username });//set user
      } catch (err) {
        localStorage.removeItem('access_token');
      }
    }
  }, []);
  const fetchStudentData = async () => {
    const token = localStorage.getItem('access_token');
    if (!token) return;
    try {
      const config = { headers: { Authorization: 'Bearer ${token}' }};
      const logsRes = await axios.get('http://127.0.0.1:8000/api/loga/', config);
      const placementsRes = await axios.get('http://127.0.0.1:8000/api/logs/placements/', config);
      setLogs(logsRes.data);
      setPlacements(placementsRes.data);
    } catch (err) {
      console.error('Failed to fetch student data');
    }
  };
  const handleSubmit = async (e) => {
    e.preventDefault(); // Stops the page from refreshing.
    setError('');//clear previous errors
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/token/', {
        username: username,
        password: password,
      });

      const accessToken = response.data.access;//get token
      localStorage.setItem('access_token', accessToken);//store in browser storage
      const payload = JSON.parse(atob(accessToken.split('.')[1]));//get usernme from token
       setUser({ username: payload.username });//set user
    } catch (err) {
      setError('Invalid username or password.');
    }
  };
  
  //seen on the screen if logged in.
  if (user) {
    return (
      <div style= {{ padding: '20px' }}>
        <h1>Welcome, {user.username}!</h1>
        <button onClick={() => {
          localStorage.removeItem('access_token');
          setUser(null);
        }}>
            Logout
        </button>
      </div>
    );
  }
  //show below if not logged in.
  return (
    <div style={{ padding: '20px' }}>
      <h1>Internship Login</h1>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <div>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        </div>
        <br></br>
        <div>
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        </div>
        <br></br>
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

//App available to the rest of the project.
export default App;