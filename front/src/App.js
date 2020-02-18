import React from 'react';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css'
import Products from './Products'
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

function App() {
  return (
    <Container fluid>
      <Row>
        <Col sm>
          <Products table="drinks" />
        </Col>
        <Col sm>
          <Products table="snacks" />
        </Col>
      </Row>
    </Container>
  );
}

export default App;
