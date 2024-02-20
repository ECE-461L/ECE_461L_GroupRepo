// HomePage.js
import React from 'react';
import { useNavigate } from 'react-router-dom';
import Button from './Button';

function HomePage() {
    let navigate = useNavigate(); // Hook to get the navigate function

    const goToLogin = () => {
        navigate('/login'); // Use navigate function to change the route
    };

    return (
        <div class-name="home-page">
            <h2>Home Page</h2>
            <div className="navigate-buttons">
                <Button label="Login" onClick={goToLogin} />
            </div>
        </div>
    );
}

export default HomePage;
