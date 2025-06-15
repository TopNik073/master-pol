// API configuration

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

        // If error is 403 and we haven't tried to refresh token yet
        if (error.response?.status === 403 && !originalRequest._retry) {
            originalRequest._retry = true;

            try {
                const refreshToken = localStorage.getItem('refreshToken');
                if (!refreshToken) {
                    throw new Error('No refresh token');
                }

                const { data } = await axios.post('/api/v1/auth/refresh', { token: refreshToken });
                
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

class API {
    constructor() {
        this.baseURL = '/api/admin/v1';
        this.headers = {
            'Content-Type': 'application/json',
        };
    }

    /**
     * @param {string} token
     */
    setAuthToken(token) {
        this.headers['Authorization'] = `Bearer ${token}`;
    }

    /**
     * @param {string} route
     * @param {Object} params
     * @returns {Promise<any>}
     */
    async get(route, params = {}) {
        try {
            const response = await axios.get(`${this.baseURL}${route}`, {
                headers: this.headers,
                params
            });
            return response.data;
        } catch (error) {
            throw this.handleError(error);
        }
    }

    /**
     * @param {string} route
     * @param {Object} data
     * @returns {Promise<any>}
     */
    async post(route, data = {}) {
        try {
            const response = await axios.post(`${this.baseURL}${route}`, data, {
                headers: this.headers
            });
            return response.data;
        } catch (error) {
            throw this.handleError(error);
        }
    }

    /**
     * @param {string} route
     * @param {Object} data
     * @returns {Promise<any>}
     */
    async put(route, data = {}) {
        try {
            const response = await axios.put(`${this.baseURL}${route}`, data, {
                headers: this.headers
            });
            return response.data;
        } catch (error) {
            throw this.handleError(error);
        }
    }

    /**
     * @param {string} route
     * @returns {Promise<any>}
     */
    async delete(route) {
        try {
            const response = await axios.delete(`${this.baseURL}${route}`, {
                headers: this.headers
            });
            return response.data;
        } catch (error) {
            throw this.handleError(error);
        }
    }

    /**
     * @param {Error} error
     * @returns {Error}
     */
    handleError(error) {
        if (error.response) {
            return new Error(error.response.data?.detail || 'Произошла ошибка при выполнении запроса');
        } else if (error.request) {
            return new Error('Нет ответа от сервера');
        } else {
            return new Error('Ошибка при выполнении запроса');
        }
    }
}

const api = new API();

export default api;