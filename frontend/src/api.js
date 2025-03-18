import axios from 'axios';

// Create an Axios instance
const api = axios.create({
    baseURL: '/api/',  // Base URL for API requests
    withCredentials: true,  // Ensures session authentication works
    headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
    }
});

export default api;
