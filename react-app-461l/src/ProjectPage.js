import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Button from './Button';
import TextBox from './TextBox';
import { useAuth } from './AuthContext';

function ProjectPage() {
    let navigate = useNavigate();

    const { user, signOut, updateProjectId } = useAuth();


    const handleSignOut = () => {
        signOut();
        navigate('/');
    };

    const [name, setName] = useState('');
    const [description, setDescription] = useState('');
    const [enteredProjectId, setProjectId] = useState('');
    const [message, setMessage] = useState('');

    const handleNameChange = (event) => {
        setName(event.target.value);
    };
    const handleDescriptionChange = (event) => {
        setDescription(event.target.value);
    };
    const handleProjectIdChange = (event) => {
        setProjectId(event.target.value);
        updateProjectId(event.target.value) // temporary implementation
    };

    const handleSubmit = (event) => {
        event.preventDefault();
    };

    const createNewProject = () => {
        setMessage("Create New Project button clicked");
        navigate('/checkout'); // temporary implementation
    };

    const useExistingProject = () => {
        setMessage("Use Existing Project button clicked");
        navigate('/checkout'); // temporary implementation
    };

    return (
        <div className="project-page">
            <div className="page-title">Project Page</div>
            <div className="text-container">
                <p>Welcome <strong>{user.user}</strong>!</p>
            </div>
            <form className="project-form" onSubmit={handleSubmit}>
                <TextBox label="Name" value={name} onChange={handleNameChange} type="text" placeholder="ECE 461L project"/>
                <TextBox label="Description" value={description} onChange={handleDescriptionChange} type="text" placeholder="HW checkout application"/>
                <TextBox label="Project ID" value={enteredProjectId} onChange={handleProjectIdChange} type="text" placeholder="ABC1234"/>
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

export default ProjectPage;
