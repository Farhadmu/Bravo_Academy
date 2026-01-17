import axios, { AxiosError, AxiosInstance, AxiosRequestConfig } from 'axios';
import { useWakeupStore } from '@/components/common/BackendWakeupManager';

// Create generic axios instance
const api: AxiosInstance = axios.create({
    baseURL: process.env.NEXT_PUBLIC_API_URL || 'https://online-education-platform-tdc4.onrender.com/api',
    withCredentials: true, // Crucial for sending/receiving HttpOnly cookies
    headers: {
        'Content-Type': 'application/json',
    },
});

// Helper to get CSRF token from cookies
const getCookie = (name: string): string | null => {
    if (typeof document === 'undefined') return null;
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop()?.split(';').shift() || null;
    return null;
};

// Request interceptor to add CSRF token and handle wakeup
api.interceptors.request.use(
    (config) => {
        // Handle CSRF token
        const csrfToken = getCookie('csrftoken');
        if (csrfToken && config.headers) {
            config.headers['X-CSRFToken'] = csrfToken;
        }

        // Handle cold start detection
        const isClient = typeof window !== 'undefined';
        if (isClient) {
            // Start a timer to check if request takes too long
            const timerId = setTimeout(() => {
                try {
                    useWakeupStore.getState().setWakingUp(true);
                } catch (e) {
                    console.error('Failed to set waking up state:', e);
                }
            }, 2500); // Trigger notification after 2.5s of no response

            (config as any)._wakeupTimerId = timerId;
        }

        // Authorization header is now handled automatically by HttpOnly cookies
        // But we keep this for backwards compatibility or mobile clients if needed
        const token = typeof window !== 'undefined' ? localStorage.getItem('accessToken') : null;
        if (token && !config.headers.Authorization) {
            config.headers.Authorization = `Bearer ${token}`;
        }

        return config;
    },
    (error) => Promise.reject(error)
);

// Response interceptor to handle token refresh and cleanup wakeup timer
api.interceptors.response.use(
    (response) => {
        const timerId = (response.config as any)._wakeupTimerId;
        if (timerId) {
            clearTimeout(timerId);
            try {
                useWakeupStore.getState().setWakingUp(false);
            } catch (e) {
                console.error('Failed to clear waking up state:', e);
            }
        }
        return response;
    },
    async (error: AxiosError) => {
        const originalRequest = error.config as AxiosRequestConfig & { _retry?: boolean, _wakeupTimerId?: any };

        // Cleanup timer on error too
        if (originalRequest?._wakeupTimerId) {
            clearTimeout(originalRequest._wakeupTimerId);
            try {
                useWakeupStore.getState().setWakingUp(false);
            } catch (e) {
                console.error('Failed to clear waking up state on error:', e);
            }
        }

        // If error is 401 and we haven't retried yet
        // AND it's not a login or register request (where 401 means invalid credentials/failure)
        const isAuthEndpoint = originalRequest.url?.includes('/auth/login/') || originalRequest.url?.includes('/auth/register/');

        if (error.response?.status === 401 && !originalRequest._retry && !isAuthEndpoint) {
            // Check if this is a maintenance mode logout
            const responseData = error.response?.data as { logout?: boolean } | undefined;
            if (responseData?.logout === true) {
                // User was logged out due to maintenance mode
                if (typeof window !== 'undefined') {
                    const { useAuthStore } = await import('@/store/auth');
                    localStorage.removeItem('accessToken');
                    localStorage.removeItem('refreshToken');
                    useAuthStore.setState({ user: null, accessToken: null, isAuthenticated: false });

                    // Redirect to login with maintenance message
                    window.location.href = '/login';
                }
                return Promise.reject(error);
            }

            originalRequest._retry = true;

            try {
                const refreshToken = localStorage.getItem('refreshToken');
                if (!refreshToken) {
                    throw new Error('No refresh token');
                }

                // Try to refresh token
                // We don't necessarily need to send 'refresh' in body anymore as it is in cookies,
                // but the backend view CookieTokenRefreshView handles both for compatibility.
                const response = await axios.post(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'}/auth/refresh/`, {}, {
                    withCredentials: true
                });

                const { access } = response.data;
                // We still update local storage/state for immediate UI responsiveness 
                // until we fully migrate the auth store to be cookie-aware.
                if (access) {
                    localStorage.setItem('accessToken', access);
                }

                if (originalRequest.headers) {
                    // Inject the new access token into the retried request
                    // even though it's also in the cookie now
                    originalRequest.headers.Authorization = `Bearer ${access}`;
                }

                return api(originalRequest);
            } catch (refreshError) {
                if (typeof window !== 'undefined') {
                    const { useAuthStore } = await import('@/store/auth');
                    localStorage.removeItem('accessToken');
                    localStorage.removeItem('refreshToken');
                    useAuthStore.setState({ user: null, accessToken: null, isAuthenticated: false });

                    // Only redirect if we're not already on the login page to avoid refresh loop
                    if (window.location.pathname !== '/login') {
                        window.location.href = '/login';
                    }
                }
                return Promise.reject(refreshError);
            }
        }
        return Promise.reject(error);
    }
);

export default api;
