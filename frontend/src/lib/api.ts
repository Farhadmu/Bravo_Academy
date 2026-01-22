import axios, { AxiosError, AxiosInstance, AxiosRequestConfig } from 'axios';

// Create generic axios instance
const getBaseURL = () => {
    // CRITICAL: Use environment variable first, fallback to Singapore for production visibility
    let url = process.env.NEXT_PUBLIC_API_URL || 'https://online-education-platform-fypx.onrender.com/api';

    // Diagnostic logging for the user to see in their browser console
    if (typeof window !== 'undefined') {
        console.log(`%c[NETWORK] Connected to: ${url}`, 'color: #00ff00; font-weight: bold;');
        if (url.includes('tdc4.onrender.com')) {
            console.error('[WARNING] Browser is still hitting OLD Oregon server!');
        }
    }

    // Normalize: remove trailing slash
    url = url.replace(/\/$/, '');

    // Ensure URL always has /api suffix if missing
    if (!url.endsWith('/api') && !url.includes('/api/')) {
        url = url + '/api';
    }

    return url;
};

const api: AxiosInstance = axios.create({
    baseURL: getBaseURL(),
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

// Request interceptor to add CSRF token
api.interceptors.request.use(
    (config) => {
        // Handle CSRF token
        const csrfToken = getCookie('csrftoken');
        if (csrfToken && config.headers) {
            config.headers['X-CSRFToken'] = csrfToken;
        }

        // Authorization header with Bearer token
        const token = typeof window !== 'undefined' ? localStorage.getItem('accessToken') : null;
        if (token && !config.headers.Authorization) {
            config.headers.Authorization = `Bearer ${token}`;
        }

        return config;
    },
    (error) => Promise.reject(error)
);

// Response interceptor to handle token refresh
api.interceptors.response.use(
    (response) => {
        return response;
    },
    async (error: AxiosError) => {
        const originalRequest = error.config as AxiosRequestConfig & { _retry?: boolean };

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
                const response = await axios.post(`${getBaseURL()}/auth/refresh/`, {}, {
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
