// Notification types and their icons
const NOTIFICATION_TYPES = {
    success: {
        icon: 'check-circle',
        color: 'var(--green)'
    },
    error: {
        icon: 'x-circle',
        color: '#ef4444'
    },
    info: {
        icon: 'info',
        color: '#3b82f6'
    }
};

// Show notification
function showNotification(message, type = 'info', duration = 5000) {
    const notificationsContainer = document.getElementById('notifications');
    const notification = document.createElement('div');
    const notificationType = NOTIFICATION_TYPES[type] || NOTIFICATION_TYPES.info;

    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <div class="notification-icon">
            <i data-lucide="${notificationType.icon}" style="color: ${notificationType.color}"></i>
        </div>
        <div class="notification-content">
            <p class="notification-message">${message}</p>
        </div>
        <button class="notification-close" onclick="removeNotification(this.parentElement)">
            <i data-lucide="x"></i>
        </button>
    `;

    notificationsContainer.appendChild(notification);
    lucide.createIcons(notification);

    // Auto remove after duration
    if (duration > 0) {
        setTimeout(() => {
            removeNotification(notification);
        }, duration);
    }

    return notification;
}

// Remove notification with animation
function removeNotification(notification) {
    if (!notification) return;

    notification.classList.add('hiding');
    notification.addEventListener('animationend', () => {
        notification.remove();
    });
}

// Clear all notifications
function clearNotifications() {
    const notificationsContainer = document.getElementById('notifications');
    notificationsContainer.innerHTML = '';
} 