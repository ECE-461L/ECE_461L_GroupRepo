import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Button from './Button';
import TextBox from './TextBox';
import { useAuth } from './AuthContext';

function CheckoutPage() {
    let navigate = useNavigate();

    const [request1, setRequest1] = useState('');
    const [request2, setRequest2] = useState('');
    const { user, signOut, projectId, updateProjectId } = useAuth();
    const [message, setMessage] = useState('');


    const handleSignOut = () => {
        signOut();
        navigate('/');
    };

    const goToProjects = () => {
        updateProjectId(null);
        navigate('/project');
    };


    const handleRequest1Change = (event) => {
        setRequest1(event.target.value);
    };

    const handleRequest2Change = (event) => {
        setRequest2(event.target.value);
    };

    const handleSubmit = (event) => {
        event.preventDefault();
    };

    const checkIn = () => {
        setMessage("Check in button clicked");
    };

    const checkOut = () => {
        setMessage("Check out button clicked");
    };

    return (
        <div className="checkout-page">
            <div className="page-title">Checkout Page</div>
            <div className="text-container">
                <p>Project ID: <strong>{projectId}</strong> </p>
            </div>
            <form className="checkout-form" onSubmit={handleSubmit}>
                <div className="grid-container">
                    <div></div>
                    <div className="grid-header">Capacity</div>
                    <div className="grid-header">Availability</div>
                    <div className="grid-header">Request</div>
                    <div className="grid-header">HW Set 1</div>
                    <div className="grid-item">100</div>
                    <div className="grid-item">100</div>
                    <div className="grid-item">
                        <TextBox label="" value={request1} onChange={handleRequest1Change} type="text" placeholder="Enter request quantity" />
                    </div>
                    <div className="grid-header">HW Set 2</div>
                    <div className="grid-item">1000</div>
                    <div className="grid-item">1000</div>
                    <div className="grid-item">
                        <TextBox label="" value={request2} onChange={handleRequest2Change} type="text" placeholder="Enter request quantity" />
                    </div>
                </div>
                <Button label="Check in" onClick={checkIn} type="button" />
                <Button label="Check out" onClick={checkOut} type="button" />
                {message && <p>{message}</p>}
            </form>
            <div className="navigate-buttons">
                <Button label="Back to project page" onClick={goToProjects} />
                <Button label="Sign out" onClick={handleSignOut} />
            </div>
        </div>
    );
}

export default CheckoutPage;
