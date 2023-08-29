import { useState } from "react";
import "./App.css";
import { ToastContainer, toast } from 'react-toastify';

function App() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState([]);
  const [currentUser, setCurrentUser] = useState(null);

  const handleSubmit = (e) => {
    e.preventDefault();


    login({ username: username, password: password })
  };

  const login = async (credenciales) => {
    try {
      const response = await fetch('http://localhost:5000/api/login', {
        method: 'POST',
        body: JSON.stringify(credenciales),
        headers: {
          'Content-Type': 'application/json'
        }
      })
      const data = await response.json()
      if (data.error) {
        toast.error(data.error)
      } else {

        toast.success(data.success)
        setCurrentUser(data)
        setUsername('')
        setPassword('')
      }

      console.log('data', data)
    } catch (error) {
      console.log(error.message)
    }
  }

  return (
    <div className="container">

      {!!currentUser ? (
        <>
          <h4>{currentUser.user.username}</h4>
          <h3>{currentUser.access_token}</h3>
        </>
      ) : (

        <form onSubmit={handleSubmit}>
          <input type="email" name="username" id="username" autoComplete="off" value={username} placeholder="Username" onChange={(e) => setUsername(e.target.value)} />
          <input type="password" name="password" autoComplete="off" id="password" value={password} placeholder="Password" onChange={(e) => setPassword(e.target.value)} />
          <button>Login</button>
        </form>
      )
      }
      <ToastContainer />
    </div>
  )
}

export default App;
