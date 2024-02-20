import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Button from './Button';

import TextBox from './TextBox'; // Adjust the path as necessary

function LoginPage() {
    const [message, setMessage] = useState('');

    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');


    let navigate = useNavigate(); // Hook to get the navigate function

    const goToHome = () => {
        navigate('/'); // Use navigate function to change the route
    };

    const handleSignInClick = () => {
        setMessage('Signing in...');
    };

    const handleSignUpClick = () => {
        setMessage('Signing up...');
    };

    const handleUsernameChange = (event) => {
        setUsername(event.target.value);
    };
    const handlePasswordChange = (event) => {
        setPassword(event.target.value);
    };
    
    

    const handleSubmit = (event) => {
        event.preventDefault();
        console.log('Submitting username:', username);
        console.log('Submitting password:', password);
    };

    const handleSignIn = (event) => {
        handleSignInClick();
        handleSubmit(event);
    };

    const handleSignUp = (event) => {
        handleSignUpClick();
        handleSubmit(event);
    };
    

    return (
        <div className="login-page">
            <h2>Login Page</h2>
            <p>{message}</p>
            
            <form onSubmit={handleSubmit} className="login-form">
                <TextBox label="Username: " value={username} onChange={handleUsernameChange} />
                <TextBox label="Password: " value={password} onChange={handlePasswordChange} />

                <Button label="Sign in" onClick={handleSignIn} />
                <Button label="Sign Up" onClick={handleSignUp} />

            </form>
            <div className="navigate-buttons">
                <Button label="Go to homepage" onClick={goToHome} />
            </div>
        </div>
    
    );
}

export default LoginPage;
