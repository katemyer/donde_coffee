import React, {useEffect, useState} from 'react';
import logo from './logo.svg';
import './App.css';
import { Users } from "./components/Users";

function App() {
  const [users, setUsers] = useState([]);

  // /GET /users for list of users
  useEffect(() => {
    fetch('/users').then(response =>
      response.json().then(data => {
      setUsers(data.users);
    })
    );
  }, []);
  console.log(users);

  return (
  
    <div className="App">
      <div className="App-header">
        DONDE COFFEE
      </div>
      <Users users={users} />
    </div>
  );
}



export default App;
