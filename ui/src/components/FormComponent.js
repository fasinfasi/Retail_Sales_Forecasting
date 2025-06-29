import React, { useState } from 'react';

const initialInput = {
  price: '',
  stock_available: '',
  date: '',
  product_category: '',
  store_location: '',
};

const categories = ['Beverage', 'Dairy', 'Frozen', 'Household', 'Snack'];
const locations = ['Los Angeles', 'New York', 'Chicago'];

// Determine API URL based on environment
const getApiUrl = () => {
  // Check if we're running in development mode
  if (process.env.NODE_ENV === 'development') {
    return 'http://localhost:8001';
  }
  
  // Check if we're running inside Docker (Docker sets this hostname)
  if (window.location.hostname === 'localhost' && process.env.REACT_APP_API_URL) {
    return process.env.REACT_APP_API_URL;
  }
  
  // For Docker Compose, use the service name
  // This might not work from browser, so we'll handle it differently
  return 'http://3.110.195.53:8001';
};

const API_BASE_URL = getApiUrl();

function isValidDate(dateString) {
  const date = new Date(dateString);
  return (
    !isNaN(date) &&
    dateString.length === 10 &&
    date.getFullYear() > 1900 &&
    date.getMonth() >= 0 &&
    date.getDate() > 0 &&
    date.getDate() <= 31
  );
}

function Form() {
  const [formData, setFormData] = useState(initialInput);
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validate date
    if (!isValidDate(formData.date)) {
      setError('Please enter a valid date (YYYY-MM-DD).');
      return;
    }

    // Validate other fields
    if (!formData.product_category || !formData.store_location) {
      setError('Please select both product category and store location.');
      return;
    }

    const [year, month, day] = formData.date.split('-').map(Number);

    const payload = {
      price: parseFloat(formData.price),
      stock_available: parseFloat(formData.stock_available),
      day,
      month,
      year,
      product_category: formData.product_category,
      store_location: formData.store_location,
    };

    try {
      const res = await fetch(`${API_BASE_URL}/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }

      const data = await res.json();
      if (data.prediction !== undefined) {
        setPrediction(Math.round(data.prediction));
        setError('');
      } else {
        setPrediction(null);
        setError(data.error || 'Unexpected error from server.');
      }
    } catch (err) {
      setPrediction(null);
      console.log('API URL used:', `${API_BASE_URL}/predict`);
      setError('Network error: ' + err.message);
    }
  };
 
  return (
    <form onSubmit={handleSubmit} style={{
      maxWidth: 500,
      margin: '40px auto',
      padding: 24,
      borderRadius: 12,
      boxShadow: '0 2px 12px rgba(0,0,0,0.08)',
      background: '#fff',
      fontFamily: 'Segoe UI, Arial, sans-serif'
    }}>
      <h2 style={{textAlign: 'center', marginBottom: 24}}>Retail Sales Forecast</h2>

      <label style={{display: 'block', marginBottom: 12}}>
        Date:
        <input
          name="date"
          type="date"
          value={formData.date}
          onChange={handleChange}
          required
          style={{marginLeft: 8, padding: 6, borderRadius: 4, border: '1px solid #ccc'}}
        />
      </label>

      <label style={{display: 'block', marginBottom: 12}}>
        Store Location:
        <select
          name="store_location"
          value={formData.store_location}
          onChange={handleChange}
          required
          style={{marginLeft: 8, padding: 6, borderRadius: 4, border: '1px solid #ccc'}}
        >
          <option value="">Select Store</option>
          {locations.map(loc => (
            <option key={loc} value={loc}>{loc}</option>
          ))}
        </select>
      </label>

      <label style={{display: 'block', marginBottom: 12}}>
        Product Category:
        <select
          name="product_category"
          value={formData.product_category}
          onChange={handleChange}
          required
          style={{marginLeft: 8, padding: 6, borderRadius: 4, border: '1px solid #ccc'}}
        >
          <option value="">Select Category</option>
          {categories.map(cat => (
            <option key={cat} value={cat}>{cat}</option>
          ))}
        </select>
      </label>

      <label style={{display: 'block', marginBottom: 12}}>
        Price:
        <input
          name="price"
          type="number"
          value={formData.price}
          onChange={handleChange}
          required
          min="0"
          step="0.01"
          style={{marginLeft: 8, padding: 6, borderRadius: 4, border: '1px solid #ccc'}}
        />
      </label>

      <label style={{display: 'block', marginBottom: 12}}>
        Stock Available:
        <input
          name="stock_available"
          type="number"
          value={formData.stock_available}
          onChange={handleChange}
          required
          min="0"
          step="1"
          style={{marginLeft: 8, padding: 6, borderRadius: 4, border: '1px solid #ccc'}}
        />
      </label>

      {error && <div style={{color: 'red', marginBottom: 12}}>{error}</div>}

      <button type="submit" style={{
        width: '100%',
        padding: 12,
        borderRadius: 6,
        border: 'none',
        background: '#007bff',
        color: '#fff',
        fontWeight: 'bold',
        fontSize: 16,
        cursor: 'pointer'
      }}>
        Predict Units Sold
      </button>

      {prediction !== null && (
        <div style={{
          marginTop: 24,
          padding: 16,
          background: '#f6f8fa',
          borderRadius: 8,
          textAlign: 'center',
          fontWeight: 'bold',
          fontSize: 16
        }}>
          📦 Estimated Units Sold on ({formData.date}):{' '}
          <span style={{ color: '#2108E1' }}>{prediction}</span>
        </div>
      )}

    </form>
  );
}

export default Form;