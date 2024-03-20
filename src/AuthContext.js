// AuthContext.js
import React, { createContext, useContext, useState } from 'react';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [projectContext, setProject] = useState(null);


  const signIn = (userData) => {
    setUser(userData);
  };

  const signOut = () => {
    setUser(null);
    setProject(null);
  };

  const updateProject = (project) => {
    setProject(project);
  };

  return (
    <AuthContext.Provider value={{ user, signIn, signOut, projectContext, updateProject }}>
      {children}
    </AuthContext.Provider>
  );
};