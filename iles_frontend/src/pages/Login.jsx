import {useState} from 'react';
import API from '../services/api';
import {useNavigate} from 'react-router-dom';


function Login() {
    const[form, setForm] = useState({
        username: "",
        password: "",
   });

    const[error, setError] = useState("");
    const navigate = useNavigate();

    const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

    const handleSubmit = async (e) => {
        e.preventDefault();

        console.log("FINAL SUBMIT FORM:", form);

        try {
            const response = await API.post("api/token/", form);
            localStorage.setItem("token", response.data.access);
            localStorage.setItem("refresh", response.data.refresh_token);

            navigate("/");

        } catch  (err) { 
          console.log(err.response?.data || err.message);
            setError("Invalid username or password");
        }
    };

    return (
    <div>
      <h1>Login</h1>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <form onSubmit={handleSubmit}>
        <input
        type="text"
      name="username"
      value={form.username}
      onChange={handleChange}
      placeholder="Username"
    />

    <input
          type="password"
          name="password"
          value={form.password}
          onChange={handleChange}
          placeholder="Password"
        />

        <button type="submit">Login</button>
      </form>

      </div>
  );
}

export default Login;