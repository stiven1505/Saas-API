import React from 'react';
import { BrowserRouter, Routes, Route, Navigate, Outlet } from 'react-router-dom';
import { useAuthStore } from './store/authStore';

import Layout from './components/Layout';
import Login from './features/Login';
import WorkspaceSelector from './features/WorkspaceSelector';
import Dashboard from './features/Dashboard';

// Protected Route Wrapper
const ProtectedRoute = () => {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated());

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
};

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />

        {/* Protected layout wrapper */}
        <Route element={<ProtectedRoute />}>
          <Route element={<Layout />}>
            <Route index element={<Dashboard />} />
            <Route path="workspaces" element={<WorkspaceSelector />} />
          </Route>
        </Route>

      </Routes>
    </BrowserRouter>
  );
}

export default App;
