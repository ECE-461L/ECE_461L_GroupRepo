// This file includes a button component that will be reused throughout the code
import React from 'react'
import './App.css'

function Button({ label, onClick }) {
    return (
        <button className="custom-button" onClick={onClick}>
            {label}
        </button>
    );
}

export default Button;