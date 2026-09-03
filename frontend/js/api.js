const API_BASE = '/api'; // Adjust base URL as needed

const api = {
    async request(endpoint, options = {}) {
        const token = localStorage.getItem('token');
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        // If body is FormData, remove Content-Type to let browser set it with boundary
        if (options.body instanceof FormData) {
            delete headers['Content-Type'];
        }

        try {
            const response = await fetch(`${API_BASE}${endpoint}`, { ...options, headers });
            
            if (!response.ok) {
                if (response.status === 401) {
                    localStorage.removeItem('token');
                    window.location.href = 'index.html';
                }
                const errData = await response.json().catch(() => ({}));
                throw new Error(errData.message || 'API request failed');
            }
            
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },

    get(endpoint) {
        return this.request(endpoint);
    },

    post(endpoint, data) {
        const options = { method: 'POST' };
        if (data instanceof FormData) {
            options.body = data;
        } else {
            options.body = JSON.stringify(data);
        }
        return this.request(endpoint, options);
    }
};
