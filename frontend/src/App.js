import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import Sidebar from './components/Sidebar';
import Tile from './components/Tile'

const App = () => {
  return (
    <div className='App'>
    <Sidebar />
    <Tile />
    </div>
  );
}

export default App;



/* 
  const loggedIn = true;
  const name = "Simon";
      {loggedIn ? (
        <>
        <h4>Hello {name}! How are you today?</h4>
        </>
      ) : (
        <>
        <h1>You are not logged in.</h1>
        </>
      )}
*/