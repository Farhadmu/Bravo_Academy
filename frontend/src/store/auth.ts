import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export interface User {
    id: string;
    username: string;
    email: string;
    full_name?: string;
    role: 'admin' | 'student' | 'staff' | 'developer';
}

interface AuthState {
    user: User | null;
    accessToken: string | null;
    isAuthenticated: boolean;
    login: (user: User, accessToken: string) => void;
    logout: () => void;
    updateUser: (user: Partial<User>) => void;
}

export const useAuthStore = create<AuthState>()(
    persist(
        (set) => ({
            user: null,
            accessToken: null,
            isAuthenticated: false,
            login: (user, accessToken) => {
                localStorage.setItem('accessToken', accessToken);
                set({ user, accessToken, isAuthenticated: true });
            },
            logout: async () => {
                try {
                    const api = (await import('@/lib/api')).default;
                    await api.post('/auth/logout/');
                } catch (error) {
                    console.error('Logout API call failed:', error);
                } finally {
                    localStorage.removeItem('accessToken');
                    set({ user: null, accessToken: null, isAuthenticated: false });
                }
            },
            updateUser: (userData) => {
                set((state) => ({
                    user: state.user ? { ...state.user, ...userData } : null,
                }));
            },
        }),
        {
            name: 'auth-storage',
            partialize: (state) => ({ user: state.user, isAuthenticated: state.isAuthenticated }),
        }
    )
);
