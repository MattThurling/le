import axios from 'axios';

const api = axios.create({
    baseURL: '/api/', 
    withCredentials: true,  // Ensures session authentication works
    headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
    }
});

// ✅ Interceptor to add CSRF token dynamically before each request
api.interceptors.request.use(
    async (config) => {
        // Get CSRF token from the DOM
        const el = document.getElementById('vue-app')
        const data = {...el.dataset}
        if (data) {            
            config.headers['X-CSRFToken'] = data.token;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

export default api;
