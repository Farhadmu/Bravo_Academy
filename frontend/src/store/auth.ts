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
    isAuthenticated: boolean;
    accessToken: string | null;
    refreshToken: string | null;
    login: (user: User, accessToken?: string, refreshToken?: string) => void;
    setTokens: (accessToken?: string, refreshToken?: string) => void;
    logout: () => void;
    updateUser: (user: Partial<User>) => void;
}

export const useAuthStore = create<AuthState>()(
    persist(
        (set) => ({
            user: null,
            isAuthenticated: false,
            accessToken: null,
            refreshToken: null,
            login: (user, accessToken, refreshToken) => {
                set({ user, isAuthenticated: true, accessToken: accessToken ?? null, refreshToken: refreshToken ?? null });
            },
            setTokens: (accessToken, refreshToken) => {
                set((state) => ({
                    accessToken: accessToken ?? state.accessToken,
                    refreshToken: refreshToken ?? state.refreshToken,
                }));
            },
            logout: async () => {
                try {
                    const api = (await import('@/lib/api')).default;
                    const storedRefresh = useAuthStore.getState().refreshToken;
                    await api.post('/auth/logout/', storedRefresh ? { refresh_token: storedRefresh } : {});
                } catch (error) {
                    console.error('Logout API call failed:', error);
                } finally {
                    set({ user: null, isAuthenticated: false, accessToken: null, refreshToken: null });
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
            partialize: (state) => ({
                user: state.user,
                isAuthenticated: state.isAuthenticated,
                accessToken: state.accessToken,
                refreshToken: state.refreshToken,
            }),
        }
    )
);
