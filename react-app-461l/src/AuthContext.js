// AuthContext.js
import React, { createContext, useContext, useState } from 'react';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [projectId, setProjectId] = useState(null);


  const signIn = (userData) => {
    setUser(userData);
  };

  const signOut = () => {
    setUser(null);
    setProjectId(null);
  };

  const updateProjectId = (id) => {
    setProjectId(id);
  };

  return (
    <AuthContext.Provider value={{ user, signIn, signOut, projectId, updateProjectId }}>
      {children}
    </AuthContext.Provider>
  );
};
