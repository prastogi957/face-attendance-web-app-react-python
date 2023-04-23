import React from "react";
import MasterComponent from "./MasterComponent";
import "./App.css";
import LoginComponent from "./LoginComponent";
import Header from "./Header";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import { Link } from "react-router-dom";
import { Container } from "react-bootstrap";


function App() {
  return (
    // <>
    // <Header />
    <div className="app">
       <Router>
    <Navbar bg="primary" variant="dark" fixed='top' className='Header'>
    <Container>
      <Navbar.Brand href="#home">Face Authentication</Navbar.Brand>
      <Nav className="me-auto">
            <Link to="">Register</Link>
            <Link to="login">Login</Link>
      </Nav>
    </Container>
  </Navbar>
  <Routes>
    <Route path="" element={<MasterComponent/>} />
    <Route path='login' element={<LoginComponent/>} />
  </Routes>
  </Router>
    </div>
    // </>
  );
}

export default App;
