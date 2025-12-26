import axios, { AxiosError, AxiosInstance, AxiosRequestConfig } from 'axios';

// Create generic axios instance
const api: AxiosInstance = axios.create({
    baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api',
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor to add auth token
api.interceptors.request.use(
    (config) => {
        // Handle cold start detection
        const isClient = typeof window !== 'undefined';
        if (isClient) {
            const { useWakeupStore } = require('@/components/common/BackendWakeupManager');

            // Start a timer to check if request takes too long
            const timerId = setTimeout(() => {
                useWakeupStore.getState().setWakingUp(true);
            }, 2500); // Trigger notification after 2.5s of no response

            (config as any)._wakeupTimerId = timerId;
        }

        const token = typeof window !== 'undefined' ? localStorage.getItem('accessToken') : null;
        if (token) {
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
            const { useWakeupStore } = require('@/components/common/BackendWakeupManager');
            useWakeupStore.getState().setWakingUp(false);
        }
        return response;
    },
    async (error: AxiosError) => {
        const originalRequest = error.config as AxiosRequestConfig & { _retry?: boolean, _wakeupTimerId?: any };

        // Cleanup timer on error too
        if (originalRequest?._wakeupTimerId) {
            clearTimeout(originalRequest._wakeupTimerId);
            const { useWakeupStore } = require('@/components/common/BackendWakeupManager');
            useWakeupStore.getState().setWakingUp(false);
        }

        // If error is 401 and we haven't retried yet
        // AND it's not a login or register request (where 401 means invalid credentials/failure)
        const isAuthEndpoint = originalRequest.url?.includes('/auth/login/') || originalRequest.url?.includes('/auth/register/');

        if (error.response?.status === 401 && !originalRequest._retry && !isAuthEndpoint) {
            originalRequest._retry = true;

            try {
                const refreshToken = localStorage.getItem('refreshToken');
                if (!refreshToken) {
                    throw new Error('No refresh token');
                }

                // Try to refresh token
                const response = await axios.post(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'}/auth/refresh/`, {
                    refresh: refreshToken,
                });

                const { access, refresh } = response.data;
                localStorage.setItem('accessToken', access);
                if (refresh) {
                    localStorage.setItem('refreshToken', refresh);
                }

                if (originalRequest.headers) {
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
