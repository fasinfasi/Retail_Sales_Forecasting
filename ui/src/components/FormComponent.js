import React, { useState } from 'react';

const initialInput = {
  price: '',
  stock_available: '',
  revenue: '',
  day: '',
  month: '',
  year: '',

  store_id_str_02: 0,
  store_id_str_03: 0,

  product_id_pdt_002: 0,
  product_id_pdt_003: 0,
  product_id_pdt_004: 0,
  product_id_pdt_005: 0,

  product_category_Dairy: 0,
  product_category_Frozen: 0,
  product_category_Household: 0,
  product_category_Snack: 0,

  store_location_Los_Angeles: 0,
  store_location_New_York: 0,

  weekday_Monday: 0,
  weekday_Saturday: 0,
  weekday_Thursday: 0,
  weekday_Tuesday: 0,
  weekday_Wednesday: 0,
};

function Form() {
  const [formData, setFormData] = useState(initialInput);
  const [prediction, setPrediction] = useState(null);

  const handleChange = (e) => {
    const { name, value, type } = e.target;
    let val = type === 'number' ? parseFloat(value) : value;
    setFormData({ ...formData, [name]: isNaN(val) ? '' : val });
  };

  const handleSelectChange = (group, options, selected) => {
    const updated = { ...formData };
    options.forEach(option => updated[option] = option === selected ? 1 : 0);
    setFormData(updated);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await fetch('http://localhost:8001/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData),
    });

    const data = await res.json();
    setPrediction(data.prediction ?? `Error: ${data.error}`);
  };

  return (
    <form onSubmit={handleSubmit} style={{ maxWidth: 700, margin: 'auto' }}>
      <h2>Enter Product & Store Details</h2>

      <label>Price: <input name="price" type="number" value={formData.price} onChange={handleChange} required /></label><br/>
      <label>Stock Available: <input name="stock_available" type="number" value={formData.stock_available} onChange={handleChange} required /></label><br/>
      <label>Revenue: <input name="revenue" type="number" value={formData.revenue} onChange={handleChange} required /></label><br/>

      <h3>Date Info</h3>
      <label>Day: <input name="day" type="number" value={formData.day} onChange={handleChange} required /></label><br/>
      <label>Month: <input name="month" type="number" value={formData.month} onChange={handleChange} required /></label><br/>
      <label>Year: <input name="year" type="number" value={formData.year} onChange={handleChange} required /></label><br/>

      <h3>Store ID</h3>
      <select onChange={e => handleSelectChange('store_id', ['store_id_str_02', 'store_id_str_03'], e.target.value)} required>
        <option value="">Select Store ID</option>
        <option value="store_id_str_02">Store 02</option>
        <option value="store_id_str_03">Store 03</option>
      </select><br/>

      <h3>Product ID</h3>
      <select onChange={e => handleSelectChange('product_id', ['product_id_pdt_002', 'product_id_pdt_003', 'product_id_pdt_004', 'product_id_pdt_005'], e.target.value)} required>
        <option value="">Select Product ID</option>
        <option value="product_id_pdt_002">PDT 002</option>
        <option value="product_id_pdt_003">PDT 003</option>
        <option value="product_id_pdt_004">PDT 004</option>
        <option value="product_id_pdt_005">PDT 005</option>
      </select><br/>

      <h3>Product Category</h3>
      <select onChange={e => handleSelectChange('product_category', ['product_category_Dairy', 'product_category_Frozen', 'product_category_Household', 'product_category_Snack'], e.target.value)} required>
        <option value="">Select Category</option>
        <option value="product_category_Dairy">Dairy</option>
        <option value="product_category_Frozen">Frozen</option>
        <option value="product_category_Household">Household</option>
        <option value="product_category_Snack">Snack</option>
      </select><br/>

      <h3>Store Location</h3>
      <select onChange={e => handleSelectChange('store_location', ['store_location_Los_Angeles', 'store_location_New_York'], e.target.value)} required>
        <option value="">Select Location</option>
        <option value="store_location_Los_Angeles">Los Angeles</option>
        <option value="store_location_New_York">New York</option>
      </select><br/>

      <h3>Weekday</h3>
      <select onChange={e => handleSelectChange('weekday', ['weekday_Monday', 'weekday_Saturday', 'weekday_Thursday', 'weekday_Tuesday', 'weekday_Wednesday'], e.target.value)} required>
        <option value="">Select Weekday</option>
        <option value="weekday_Monday">Monday</option>
        <option value="weekday_Tuesday">Tuesday</option>
        <option value="weekday_Wednesday">Wednesday</option>
        <option value="weekday_Thursday">Thursday</option>
        <option value="weekday_Saturday">Saturday</option>
      </select><br/><br/>

      <button type="submit">Predict Sales</button>

      {prediction !== null && (
        <div style={{ marginTop: '20px', fontWeight: 'bold' }}>
          Prediction: {prediction}
        </div>
      )}
    </form>
  );
}

export default Form;
