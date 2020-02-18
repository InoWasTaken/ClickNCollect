import React, { useState } from 'react';
import Table from 'react-bootstrap/Table';
import ProductsRow from './ProductsRow'

let tableau_test = [
    {
        "in_stock": 0,
        "name": "coca",
        "rowid": 1
    },
    {
        "in_stock": 1,
        "name": "ice tea",
        "rowid": 2
    }]

function Products(props) {
    const [products, setProducts] = useState(tableau_test)
    function switchDisponibility(id) {
        const product = products.find((p) => p.rowid === id)
        product.in_stock = product.in_stock === 1 ? 0 : 1
        setProducts([...products])
    }
    console.log(products)
    return (
        <Table striped bordered hover>
            <thead>
                <tr>
                    <th>{props.table === 'drinks' ? "Boissons" : "Snacks"}</th>
                    <th>Disponibilité</th>
                </tr>
            </thead>
            <tbody>
                {products.map((product) =>
                    <ProductsRow
                        key={product.rowid}
                        product={product}
                        onChange={switchDisponibility} />
                )}
            </tbody>
        </Table>
    );
}

export default Products