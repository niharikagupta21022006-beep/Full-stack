import {useState,useEffect} from 'react';

function App() {
  const[orders,setOrders] = useState([]);
  const[price,setPrice] = useState('');
  const[quantity,setQuantity] = useState('');
  const[side,setSide] = useState('BUY');

  const fetchOrders = () => {
    fetch('http://127.0.0.1:8000/api/orders')
    .then(response => response.json())
    .then(data => setOrders(data));
  };

  useEffect(() => {
    fetchOrders();
  },[]);

  const handleSubmit = (e) => {
    e.preventDefault();

    fetch('http://127.0.0.1:8000/api/orders/',{
      method:'POST',
      headers:{
        'Content-Type':'application/json',
      },

      body:JSON.stringify({
        price:price,
        quantity:quantity,
        side:side,
      }),
    })

    .then(response => response.json())
    .then(() => {
      fetchOrders();
      setPrice('');
      setQuantity('');
    });
  };

  return (
    <div>
      <h1>Order Book</h1>
      <form onSubmit={handleSubmit}>
        <input
        type="number"
        placeholder="Price"
        value={price}
        onChange={(e) => setPrice(e.target.value)}
        />

        <input
        type="number"
        placeholder="Quantity"
        value={quantity}
        onChange={(e) => setQuantity(e.target.value)}
        />

        <select value={side} onChange={(e) =>setSide(e.target.value)}>
          <option value="BUY">BUY</option>
          <option value="SELL">SELL</option>

        </select>
        <button type="submit">Add Order</button>
      </form>


      <ul>
        {orders.map(order =>(
          <li key={order.id}>
            {order.side} {order.quantity} @ {order.price}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;