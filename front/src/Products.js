import React, { useState, useEffect } from 'react';
import Table from 'react-bootstrap/Table';
import ProductsRow from './ProductsRow'

function Products(props) {
    const [products, setProducts] = useState([])

    useEffect(() => {
        const getProducts = async () => {
            const response = await fetch(`${process.env.REACT_APP_API_HOST}/${props.table}`)
            const responseJSON = await response.json()
            setProducts(responseJSON)
        }
        getProducts()
    }, [props.table])

    async function switchDisponibility(id) {
        const product = products.find((p) => p.rowid === id)
        product.in_stock = product.in_stock === 1 ? 0 : 1
        await fetch(`${process.env.REACT_APP_API_HOST}/${props.table}/${product.rowid}`,
            {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(product)
            })
        setProducts([...products])
    }

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