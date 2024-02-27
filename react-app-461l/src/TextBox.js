import React from 'react';
import './App.css';

function TextBox({ label, value, onChange, type, placeholder}) {
  return (
    <div className="text-box-container">
      <label>{label}</label>
      <input type={type} value={value} onChange={onChange} className="custom-text-box" placeholder={placeholder} />
    </div>
  );
}

export default TextBox;
 