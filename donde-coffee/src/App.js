import React, {useEffect, useState} from 'react';
import logo from './logo.svg';
import './App.css';
import { Movies } from "./components/Movies";

function App() {
  const [movies, setMovies] = useState([]);

  useEffect(() => {
    fetch('/movies').then(response =>
      response.json().then(data => {
      setMovies(data.movies);
    })
    );
  }, []);
  console.log(movies);

  return (
    <div className="App">
  <Movies movies={movies} />
    </div>
  );
}

export default App;
