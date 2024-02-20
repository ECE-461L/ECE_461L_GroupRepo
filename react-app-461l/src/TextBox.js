import React from 'react';
import './App.css';

function TextBox({ label, value, onChange }) {
  return (
    <div className="text-box-container">
      <label>
        {label}
        <input type="text" value={value} onChange={onChange} className="custom-text-box" />
      </label>
    </div>
  );
}

export default TextBox;
