// CheckoutPage.js
import React from 'react';
import { useNavigate } from 'react-router-dom';
import Button from './Button';
import { useAuth } from './AuthContext';

function CheckoutPage() {
    let navigate = useNavigate();

    const { user, signOut } = useAuth(); // Destructure user and signOut from context

    const handleSignOut = () => {
        signOut();
        navigate('/');
    };


    return (
        <div className="checkout-page">
            <div className="page-title">
                Checkout Page
            </div>
            <div className="text-container">
                <p>
                    Welcome {user.user}! This is the Checkout Page of the hardware checkout application
                </p>
            </div>

            <div className="navigate-buttons">
                <Button label="Sign out" onClick={handleSignOut} />
            </div>
        </div>
    );
}

export default CheckoutPage;
