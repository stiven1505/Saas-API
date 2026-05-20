import { create } from 'zustand';
import { jwtDecode } from 'jwt-decode';

interface User {
  user_id: string;
  email: string;
  full_name: string;
  role: string;
}

interface AuthState {
  token: string | null;
  user: User | null;
  setToken: (token: string) => void;
  logout: () => void;
  isAuthenticated: () => boolean;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  token: localStorage.getItem('token'),
  user: localStorage.getItem('token') ? jwtDecode(localStorage.getItem('token')!) : null,
  setToken: (token: string) => {
    localStorage.setItem('token', token);
    const decoded = jwtDecode<User>(token);
    set({ token, user: decoded });
  },
  logout: () => {
    localStorage.removeItem('token');
    set({ token: null, user: null });
  },
  isAuthenticated: () => !!get().token,
}));
