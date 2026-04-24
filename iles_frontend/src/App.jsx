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
  const [message, setMessage] = useState(''); // Success/error message when creating log
  const [logs, setLogs] = useState([]); //logs of all the students
  const [placements, setPlacements] = useState([]); //placements for dropdown
  const [supervisorLogs, setSupervisorLogs] = useState([]); //logs for supervisor view 
  
  // This function runs when the form is submitted.
  const fetchStudentData = async () => {
  const token = localStorage.getItem('access_token');
  if (!token) return; //not logged in, do nothing.
  try {
    const config = { headers: { Authorization: `Bearer ${token}` }};//attach token
      //get the student's logs
    const logsRes = await axios.get('http://127.0.0.1:8000/api/logs/', config);//get placement options on dropdown
    const placementsRes = await axios.get('http://127.0.0.1:8000/api/placements/', config);
    setLogs(logsRes.data);
    setPlacements(placementsRes.data);
  } catch (err) {
    console.error('Failed to fetch student data');
  }
};

  const handleCreateLog = async (e) => {
    e.preventDefault();
    setMessage('');
    const token = localStorage.getItem('access_token');
    try {
      const config = {headers: { Authorization: `Bearer ${token}` }};
      await axios.post('http://127.0.0.1:8000/api/logs/', newLog, config);
      //clear the form
      setNewLog({ week_number: '', activities: '', placement: ''});
      setMessage('Log created successfully!');
      fetchStudentData();//refresh logs to add new log
    } catch (err) {
      setMessage('Error creating log.');
    }
  };
  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      try {
        const payload = JSON.parse(atob(token.split('.')[1]));//get usernme from token
        const userData = { username: payload.username, role: payload.role }; //get user role from token
        setUser(userData);//fetch the data of the student
        if (payload.role ==='student') {
          fetchStudentData();
        }
      } catch (err) {
        localStorage.removeItem('access_token');
      }
    }
  }, []);
//event handlers
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
      const userData = { username: payload.username, role: payload.role };//set user
      setUser(userData);
      if (payload.role === 'student') {
        fetchStudentData();
      }
    } catch (err) {
      setError('Invalid username or password.');
    }
  };
  
  //seen on the screen if logged in.
  if(user){
  if (user.role === 'student') {//student dashboard
      return (
        <div style= {{ padding: '20px' }}>
          <h1>Student Dashboard</h1>
          <p>Welcome, {user.username}!</p>
          <button onClick={() => {
            localStorage.removeItem('access_token');
            setUser(null);
            setLogs([]);
            setPlacements([]);
          }}>
              Logout
          </button>
          <h2>Create New Weekly Log</h2>
          {message && <p>{message}</p>}
          <form onSubmit={handleCreateLog}>
            <div>
              <input
                type = "number"
                placeholder = "Week No."
                value = {newLog.week_number}
                onChange = {(e) => setNewLog({ ...newLog, week_number: e.target.value })}
                required
                />
            </div>
            <br></br>
            <div>
              <textarea
                placeholder = "Activities this week"
                value = {newLog.activities}
                onChange = {(e) => setNewLog({ ...newLog, activities: e.target.value})}
                required
                />
            </div>
            <div>
              <select
                value = {newLog.placement}
                onChange = {(e) => setNewLog({ ...newLog, placement: e.target.value})}
                required>
                  <option value = "">Select Placement</option>
                  {placements.map((p) => (
                    <option key = {p.id} value = {p.id}>{p.company_name}</option>
                  ))}
                </select>
            </div>
            <br></br>
            <button type = "submit">Submit Log</button>
          </form>

        {/*My Logs*/}
        <h2>My Weekly Logs</h2>
        {logs.length === 0 ? (
          <p>No Logs Submitted yet.</p>
        ) : (
          <ul>
          {logs.map((log) => (
            <li key = {log.id}>
            Week {log.week_number}: {log.activities} - <strong>{log.status}</strong>
            /*sbmit for review button to be added*/
            </li>
          ))}
          </ul>
        )}
        </div>
      );
    }
  //Supervisor Dashboard//
  if (user.role === 'workplace_supervisor' || user.role === 'academic_supervisor') {
    return (
      <div style = {{ padding: '20px'}}>
        <h1>Supervisor Dashboard</h1>
        <p>Welcome, {user.username} ({user.role})!</p>
        <button onClick = {() => {
          localStorage.removeItem('access_token');
          setUser(null);
          setSupervisorLogs([]); //clear logs on logout
        }}>
          Logout
        </button>
      </div>
    );
  }

  //Admin Fallback//
    if (user.role === 'admin') {
      return (
        <div style =  {{ padding: '20px'}}>
          <h1>Administrator</h1>
          <button onClick = {() => {
            localStorage.removeItem('access_token');
            setUser(null);
        }}>
          Logout
        </button>
      </div>
    );
    }
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
   
export default App;