import React from 'react';
import Form from 'react-bootstrap/Form';

function ProductsRow({ product, onChange }) {
    return (
        <tr>
            <td>{product.name}</td>
            <td>
                <Form.Check
                    type="switch"
                    checked={product.in_stock}
                    id={"switch-" + product.name}
                    label=""
                    onChange={() => onChange(product.rowid)}
                /></td>
        </tr>
    )
}

export default ProductsRow