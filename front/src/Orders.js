import React, { useState, useEffect } from 'react';

function Orders() {
    const [orders, setOrders] = useState([])

    useEffect(() => {
        const getOrders = async () => {
            const response = await fetch(`${process.env.REACT_APP_API_HOST}/orders`)
            const responseJSON = await response.json()
            setOrders(responseJSON)
        }
        setInterval(getOrders, 1000)
    }, [])

    return (
        <>
            <div>Dernières commandes :</div>
            <ul>
                {orders.map(order => <li key={order.rowid}>{order.items}</li>)}
            </ul>
        </>
    )
}

export default Orders