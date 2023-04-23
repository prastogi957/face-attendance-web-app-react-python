import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import './Header.css'
import { Link, Routes } from 'react-router-dom';
import { Route,BrowserRouter as Router } from 'react-router-dom';
import MasterComponent from "./MasterComponent";
import LoginComponent from './LoginComponent';

function Header() {
  return (
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
  );
}

export default Header;