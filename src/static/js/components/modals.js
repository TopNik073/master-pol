// Modal functions
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modalId === 'profileModal') {
        const user = JSON.parse(localStorage.getItem('user'))
        if (user) {
            document.getElementById('userName').value = user.name
            document.getElementById('userEmail').value = user.email
        }
    }
    if (modal) {
        modal.style.display = 'flex';
        // Trigger reflow
        modal.offsetHeight;
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
        // Wait for animation to complete before hiding
        setTimeout(() => {
            if (!modal.classList.contains('active')) {
                modal.style.display = 'none';
            }
        }, 300);
        document.body.style.overflow = '';
    }
}

function togglePassword(inputId, button) {
    const input = document.getElementById(inputId);
    const icon = button.querySelector('.password-icon');
    
    if (!input || !icon) {
        console.error('Could not find input or icon element');
        return;
    }
    
    if (input.type === 'password') {
        input.type = 'text';
        icon.setAttribute('data-lucide', 'eye-off');
    } else {
        input.type = 'password';
        icon.setAttribute('data-lucide', 'eye');
    }
    
    // Reinitialize Lucide icons
    const icons = document.querySelectorAll('[data-lucide]');
    icons.forEach(icon => {
        lucide.createIcons(icon);
    });
}

// Close modal when clicking outside
document.addEventListener('click', (event) => {
    if (event.target.classList.contains('modal')) {
        closeModal(event.target.id);
    }
});

// Close modal on escape key
document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
        const activeModal = document.querySelector('.modal.active');
        if (activeModal) {
            closeModal(activeModal.id);
        }
    }
});