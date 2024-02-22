// HomePage.js
import React from 'react';
import { useNavigate } from 'react-router-dom';
import Button from './Button';

function HomePage() {
    let navigate = useNavigate();

    const goToLogin = () => {
        navigate('/login');
    };

    return (
        <div class-name="home-page">
            <h2 class-name="page-title">
                Home Page
            </h2>
            <div className="navigate-buttons">
                <Button label="Go to login page" onClick={goToLogin} />
            </div>
        </div>
    );
}

export default HomePage;
