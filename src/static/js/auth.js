// Auth API functions
async function login(email, password) {
    try {
        const { data } = await axios.post('/auth/login', { email, password });
        
        // Save tokens to localStorage
        localStorage.setItem('accessToken', data.data.tokens.access.token);
        localStorage.setItem('refreshToken', data.data.tokens.refresh.token);
        localStorage.setItem('user', JSON.stringify(data.data.user));

        return data;
    } catch (error) {
        throw new Error(error.response?.data?.error || 'Ошибка при входе');
    }
}

async function register(name, email, password) {
    try {
        const { data } = await axios.post('/auth/register', { 
            name, 
            email, 
            password,
            role: 'user' // Default role
        });
        
        // Save tokens to localStorage
        localStorage.setItem('accessToken', data.data.tokens.access.token);
        localStorage.setItem('refreshToken', data.data.tokens.refresh.token);
        localStorage.setItem('user', JSON.stringify(data.data.user));

        return data;
    } catch (error) {
        throw new Error(error.response?.data?.error || 'Ошибка при регистрации');
    }
}

// Form handlers
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;

    try {
        await login(email, password);
        closeModal('loginModal');
        updateAuthUI();
        showNotification('Успешный вход', 'success');
    } catch (error) {
        showNotification(error.message, 'error');
    }
});

document.getElementById('registerForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const name = document.getElementById('registerName').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    const passwordVerify = document.getElementById('registerPasswordVerify').value;

    if (password !== passwordVerify) {
        showNotification('Пароли не совпадают', 'error');
        return;
    }

    try {
        await register(name, email, password);
        closeModal('registerModal');
        updateAuthUI();
        showNotification('Успешная регистрация', 'success');
    } catch (error) {
        showNotification(error.message, 'error');
    }
});

// Profile menu functions
function toggleProfileMenu() {
    const menu = document.getElementById('profileMenu');
    menu.classList.toggle('active');
}

// Close profile menu when clicking outside
document.addEventListener('click', (e) => {
    const menu = document.getElementById('profileMenu');
    const button = document.querySelector('.profile-button');
    
    if (menu && !menu.contains(e.target) && !button.contains(e.target)) {
        menu.classList.remove('active');
    }
});

// UI update functions
function updateAuthUI() {
    const user = JSON.parse(localStorage.getItem('user'));
    const headerNonAuth = document.getElementById('headerNonAuth');
    const headerAuth = document.getElementById('headerAuth');
    const profileIcon = document.getElementById('profileIcon');
    const adminPanel = document.querySelector('.admin-only');
    
    if (user) {
        headerNonAuth.style.display = 'none';
        headerAuth.style.display = 'block';
        
        // Update profile icon color based on role
        if (user.role === 'admin') {
            profileIcon.parentElement.classList.add('admin');
            adminPanel.style.display = 'flex';
        } else {
            profileIcon.parentElement.classList.remove('admin');
            adminPanel.style.display = 'none';
        }
    } else {
        headerNonAuth.style.display = 'block';
        headerAuth.style.display = 'none';
    }
}

function logout() {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('user');
    updateAuthUI();
    showNotification('Вы вышли из системы', 'success');
}

// Fetch user data
async function fetchUserData() {
    try {
        const { data } = await axios.get('/users/me');
        localStorage.setItem('user', JSON.stringify(data.data));
        updateAuthUI();
    } catch (error) {
        console.error('Error fetching user data:', error);
        // If we get a 403, the token might be invalid
        if (error.response?.status === 403) {
            localStorage.removeItem('accessToken');
            localStorage.removeItem('refreshToken');
            localStorage.removeItem('user');
            updateAuthUI();
        }
    }
}

// Initialize UI on page load
document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('accessToken');
    if (token) {
        fetchUserData();
    } else {
        updateAuthUI();
    }
}); 