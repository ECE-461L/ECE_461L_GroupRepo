import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Button from './Button';
import TextBox from './TextBox';
import { useAuth } from './AuthContext';

function CheckoutPage() {
    let navigate = useNavigate();
    const { signOut, projectContext, updateProject } = useAuth();
    const [request1, setRequest1] = useState('');
    const [request2, setRequest2] = useState('');
    const [message, setMessage] = useState('');
    const [inputError, setInputError] = useState('');
    const onlyNumbers = /^\d+$/;

    const handleSignOut = () => {
        signOut();
        navigate('/');
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

    const goToProjects = () => {
        navigate('/project');
    };
    
    const normalizeAndValidateRequests = () => {
        const normalizedRequest1 = request1.trim() === '' ? '0' : request1;
        const normalizedRequest2 = request2.trim() === '' ? '0' : request2;
        const numRequest1 = parseInt(normalizedRequest1, 10);
        const numRequest2 = parseInt(normalizedRequest2, 10);
    
        if (numRequest1 === 0 && numRequest2 === 0) {
            setInputError("Both request quantities cannot be 0.");
            setMessage("");
            return false;
        }
    
        if (!onlyNumbers.test(normalizedRequest1) || !onlyNumbers.test(normalizedRequest2)) {
            setInputError("Request quantities must be valid numbers.");
            setMessage("");
            return false;
        }
    
        setInputError("");
        return { normalizedRequest1, normalizedRequest2 };
    };

    const performCheckOperation = async (operation) => {
        const validationResults = normalizeAndValidateRequests();
        if (!validationResults) return;
    
        try {
            const response = await fetch(`http://localhost:5000/${operation}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ 
                    request1: validationResults.normalizedRequest1, 
                    request2: validationResults.normalizedRequest2, 
                    projectId: projectContext.projectId 
                })
            });

            const projectData = await response.json();
            if (!response.ok) {
                throw new Error(projectData.message || `Default project ${operation} error`);
            }

            setMessage(projectData.message);
            updateProject(projectData);
        } catch (error) {
            setMessage("");
            setInputError(error.message);
            console.error(error);
        }
    };

    const checkIn = () => performCheckOperation('check-in');
    const checkOut = () => performCheckOperation('check-out');


    return (
        <div className="checkout-page">
            <div className="page-title">Checkout Page</div>
            <div className="text-container">
                <p>
                    Project: <strong>{projectContext.name}</strong><br />
                    ID: <strong>{projectContext.projectId}</strong>
                </p>
            </div>
            <form className="checkout-form" onSubmit={handleSubmit}>
                <div className="grid-container">
                    <div></div>
                    <div className="grid-header">Capacity</div>
                    <div className="grid-header">Availability</div>
                    <div className="grid-header">Request</div>
                    <div className="grid-header">HW Set 1</div>
                    <div className="grid-item">{projectContext.hwSet1Capacity}</div>
                    <div className="grid-item">{projectContext.hwSet1Availability}</div>
                    <div className="grid-item">
                        <TextBox label="" value={request1} onChange={handleRequest1Change} type="text" placeholder="Enter request quantity" />
                    </div>
                    <div className="grid-header">HW Set 2</div>
                    <div className="grid-item">{projectContext.hwSet2Capacity}</div>
                    <div className="grid-item">{projectContext.hwSet2Availability}</div>
                    <div className="grid-item">
                        <TextBox label="" value={request2} onChange={handleRequest2Change} type="text" placeholder="Enter request quantity" />
                    </div>
                </div>
                <Button label="Check in" onClick={checkIn} type="button" />
                <Button label="Check out" onClick={checkOut} type="button" />
            </form>
            <div>
                {inputError && <p className="error-message">{inputError}</p>}
                <p>{message}</p>
            </div>
            <div className="navigate-buttons">
                <Button label="Back to project page" onClick={goToProjects} />
                <Button label="Sign out" onClick={handleSignOut} />
            </div>
        </div>
    );
}

export default CheckoutPage;
