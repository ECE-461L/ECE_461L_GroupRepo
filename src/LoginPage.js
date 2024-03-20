import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from './AuthContext';
import Button from './Button';
import TextBox from './TextBox';


function LoginPage() {
    const backendUrl = process.env.REACT_APP_BACKEND_URL;

    console.log("backend URL used:")
    console.log(`${backendUrl}`)

    const [message, setMessage] = useState('');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [authError, setAuthError] = useState('');
    const [action, setAction] = useState(''); // Track whether the user is signing in or signing up
    const { signIn } = useAuth();

    let navigate = useNavigate();

    const goToHome = () => {
        navigate('/');
    };

    const handleUsernameChange = (event) => {
        setUsername(event.target.value);
    };
    const handlePasswordChange = (event) => {
        setPassword(event.target.value);
    };

    const authenticateUser = async () => {
        setMessage('Sign in button clicked');
        const response = await fetch(`${backendUrl}/authenticate`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.message || 'Default login error');
        }
        return data;
    };

    

    const registerUser = async () => {
        setMessage('Sign up button clicked');
        const response = await fetch(`${backendUrl}/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.message || 'Default login error');
        }
        return data;
    };

    const handleSubmit = async(event) => {
        event.preventDefault();

        if (password.length < 8) {
            setAuthError('Password must be at least 8 characters long.');
            return;
        }

        if (action === 'signIn') {
            try {
                const userData = await authenticateUser();
                if (userData) {
                    signIn(userData);
                    setMessage(userData.message);
                    navigate('/project');
                }
                // goToHome();
            } catch (error) {
                setAuthError(error.message);
                console.error(error);
            }
        }
        
        else if (action === 'signUp') {
            try {
                const userData = await registerUser();
                if (userData) {
                    signIn(userData);
                    setMessage(userData.message);
                    navigate('/project');
                }
                // goToHome();
            } catch (error) {
                setAuthError(error.message);
                console.error(error);
            }            
        }
    };

    const handleAction = (actionType) => {
        setAction(actionType); // Set the action based on the button clicked
    };


    return (
        <div className="login-page">
            <form onSubmit={handleSubmit} className="form-container">
                <TextBox label="Username: " value={username} onChange={handleUsernameChange} type="text" placeholder="user123"/>
                <TextBox label="Password: " value={password} onChange={handlePasswordChange} type="password" placeholder="password123"/>
                <Button label="Sign in" onClick={() => handleAction('signIn')} />
                <Button label="Sign Up" onClick={() => handleAction('signUp')} />
            </form>
            <div>
                {authError && <p className="error-message">{authError}</p>}
                {/* <p>{message}</p> */}
            </div>
            <div className="page-title">
                Login Page
            </div>
            <div className="navigate-buttons">
                <Button label="Go to home page" onClick={goToHome} />
            </div>
        </div>
    );
}

export default LoginPage;