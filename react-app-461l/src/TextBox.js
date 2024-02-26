import React from 'react';
import './App.css';

function TextBox({ label, value, onChange, type }) {
  return (
    <div className="text-box-container">
      <label>
        {label}
        <input type={type} value={value} onChange={onChange} className="custom-text-box" />
      </label>
    </div>
  );
}

export default TextBox;
