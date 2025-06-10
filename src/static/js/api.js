// API configuration
const API_URL = '/api/v1';

// Configure axios defaults
axios.defaults.baseURL = API_URL;
axios.defaults.headers.common['Content-Type'] = 'application/json';

// Add request interceptor for adding auth token
axios.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('accessToken');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Add response interceptor for handling token refresh
axios.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        // If error is 401 and we haven't tried to refresh token yet
        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            try {
                const refreshToken = localStorage.getItem('refreshToken');
                if (!refreshToken) {
                    throw new Error('No refresh token');
                }

                const { data } = await axios.post('/auth/refresh', { token: refreshToken });
                
                // Update tokens
                localStorage.setItem('accessToken', data.data.tokens.access.token);
                localStorage.setItem('refreshToken', data.data.tokens.refresh.token);
                localStorage.setItem('user', JSON.stringify(data.data.user));

                // Retry original request with new token
                originalRequest.headers.Authorization = `Bearer ${data.data.tokens.access.token}`;
                return axios(originalRequest);
            } catch (refreshError) {
                // If refresh fails, logout user
                if (typeof logout === 'function') {
                    logout();
                }
                return Promise.reject(refreshError);
            }
        }

        return Promise.reject(error);
    }
); 