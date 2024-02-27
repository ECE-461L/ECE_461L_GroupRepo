import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Button from './Button';
import TextBox from './TextBox';
import { useAuth } from './AuthContext';

function CheckoutPage() {
    let navigate = useNavigate();

    const { user, signOut } = useAuth();

    const handleSignOut = () => {
        signOut();
        navigate('/');
    };

    const [name, setName] = useState('');
    const [description, setDescription] = useState('');
    const [projectId, setProjectId] = useState('');
    const [message, setMessage] = useState('');

    const handleNameChange = (event) => {
        setName(event.target.value);
    };
    const handleDescriptionChange = (event) => {
        setDescription(event.target.value);
    };
    const handleProjectIdChange = (event) => {
        setProjectId(event.target.value);
    };

    const handleSubmit = (event) => {
        event.preventDefault();
    };

    const createNewProject = () => {
        setMessage("Create New Project button clicked");
    };

    const useExistingProject = () => {
        setMessage("Use Existing Project button clicked");
    };

    return (
        <div className="checkout-page">
            <div className="page-title">Checkout Page</div>
            <div className="text-container">
                <p>Welcome <strong>{user.user}</strong>! This is the Checkout Page of the hardware checkout application</p>
            </div>
            <form className="project-form" onSubmit={handleSubmit}>
                <TextBox label="Name" value={name} onChange={handleNameChange} type="text"/>
                <TextBox label="Description" value={description} onChange={handleDescriptionChange} type="text"/>
                <TextBox label="Project ID" value={projectId} onChange={handleProjectIdChange} type="text"/>
                {message && <p>{message}</p>}
                <Button label="Create New Project" onClick={createNewProject} type="button" />
                <Button label="Use Existing Project" onClick={useExistingProject} type="button" />
            </form>
            <div className="navigate-buttons">
                <Button label="Sign out" onClick={handleSignOut} type="button" />
            </div>
        </div>
    );
}

export default CheckoutPage;
