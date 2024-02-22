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
            <div className="page-title">
                Home Page
            </div>

            <div className="text-container">
                <p>
                    Welcome to the Home Page of the hardware checkout application
                </p>
            </div>

            <div className="navigate-buttons">
                <Button label="Go to login page" onClick={goToLogin} />
            </div>
        </div>
    );
}

export default HomePage;
