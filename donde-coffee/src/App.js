import React, {useEffect, useState} from 'react';
import logo from './logo.svg';
import './App.css';
import { Users } from "./components/Users";
import { Shops } from "./components/Shops";

function App() {
  const [users, setUsers] = useState([]);
  const [shops, setShops] = useState([]);

  // /GET /users for list of users
  useEffect(() => {
    fetch('/users').then(response =>
      response.json().then(data => {
      setUsers(data.users);
    })
    );
  }, []);
  console.log(users);

    // /GET /shops for list of shops
    useEffect(() => {
      fetch('/shops').then(response =>
        response.json().then(data => {
        setShops(data.shops);
      })
      );
    }, []);
    console.log(shops);

  return (
  
    <div className="App">
      <div className="App-header">
        DONDE COFFEE!
      </div>
      <Users users={users} />
      <Shops shops={shops} />
    </div>
  );
}



export default App;
