import axios from 'axios';
import { useWorkspaceStore } from '../store/workspaceStore';

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  
  const workspace = useWorkspaceStore.getState().currentWorkspace;
  if (workspace) {
    config.headers['X-Workspace-Id'] = workspace.id;
  }
  
  return config;
});

export default api;
