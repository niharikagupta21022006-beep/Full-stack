import { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [orders, setOrders] = useState([]);
  const [price, setPrice] = useState('');
  const [quantity, setQuantity] = useState('');
  const [side, setSide] = useState('BUY');
  const [isConnected, setIsConnected] = useState(false);

  const fetchOrders = () => {
    fetch('https://tradingcore-web.onrender.com/api/orders')
      .then(response => response.json())
      .then(data => setOrders(data));
  };

  useEffect(() => {
    fetchOrders();

    const socket = new WebSocket('wss://tradingcore-web.onrender.com/ws/orders/');

    socket.onmessage = function (event) {
      const newOrder = JSON.parse(event.data);
      setOrders((prevOrders) => [...prevOrders, newOrder]);
    };

    socket.onopen = function () {
      setIsConnected(true);
    };

    socket.onclose = function () {
      setIsConnected(false);
    };

    return () => {
      socket.close();
    }
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();

    fetch('https://tradingcore-web.onrender.com/api/orders/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        price: price,
        quantity: quantity,
        side: side,
      }),
    })
      .then(response => response.json())
      .then(() => {
        fetchOrders();
        setPrice('');
        setQuantity('');
      });
  };

  const buyOrders = orders.filter(o => o.side === 'BUY').sort((a, b) => b.price - a.price);
  const sellOrders = orders.filter(o => o.side === 'SELL').sort((a, b) => a.price - b.price);

  return (
    <div className="app">

      <nav className="navbar">
        <div className="logo">📈 TradingCore</div>
        <span className={`status-badge ${isConnected ? 'live' : 'offline'}`}>
          {isConnected ? '● Live' : '○ Offline'}
        </span>
      </nav>

      <div className="container">
        <h1>Order Book</h1>

        <div className="order-card">
          <form onSubmit={handleSubmit}>
            <input
              type="number"
              placeholder="Price"
              value={price}
              onChange={(e) => setPrice(e.target.value)}
              required
            />
            <input
              type="number"
              placeholder="Quantity"
              value={quantity}
              onChange={(e) => setQuantity(e.target.value)}
              required
            />
            <select value={side} onChange={(e) => setSide(e.target.value)}>
              <option value="BUY">BUY</option>
              <option value="SELL">SELL</option>
            </select>
            <button type="submit" className={side === 'BUY' ? 'btn-buy' : 'btn-sell'}>
              {side === 'BUY' ? 'Buy' : 'Sell'}
            </button>
          </form>
        </div>

        <div className="orderbook-grid">
          <div className="orderbook-card buy-card">
            <div className="card-header">
              <span>Buy Orders</span>
              <span className="count">{buyOrders.length}</span>
            </div>
            <div className="list-header">
              <span>Price</span>
              <span>Qty</span>
            </div>
            <div className="scroll-list">
              {buyOrders.map(order => (
                <div key={order.id} className="list-row">
                  <span className="price buy-price">₹{order.price}</span>
                  <span>{order.quantity}</span>
                </div>
              ))}
              {buyOrders.length === 0 && <div className="empty-state">No buy orders yet</div>}
            </div>
          </div>

          <div className="orderbook-card sell-card">
            <div className="card-header">
              <span>Sell Orders</span>
              <span className="count">{sellOrders.length}</span>
            </div>
            <div className="list-header">
              <span>Price</span>
              <span>Qty</span>
            </div>
            <div className="scroll-list">
              {sellOrders.map(order => (
                <div key={order.id} className="list-row">
                  <span className="price sell-price">₹{order.price}</span>
                  <span>{order.quantity}</span>
                </div>
              ))}
              {sellOrders.length === 0 && <div className="empty-state">No sell orders yet</div>}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;