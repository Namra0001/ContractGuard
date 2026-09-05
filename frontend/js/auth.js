document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                const res = await api.post('/auth/login', { email, password });
                localStorage.setItem('token', res.access_token || res.token);
                window.location.href = 'dashboard.html';
            } catch (err) {
                alert(err.message);
            }
        });
    }

    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                await api.post('/auth/register', { name, email, password });
                alert('Registration successful! Please login.');
                window.location.href = 'index.html';
            } catch (err) {
                alert(err.message);
            }
        });
    }
});
