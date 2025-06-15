document.addEventListener('DOMContentLoaded', () => {
    const adminAvatar = document.getElementById('admin-avatar')
    const adminName = document.getElementById('admin-name')
    const adminEmail = document.getElementById('admin-email')
    if (!adminAvatar || !adminName || !adminEmail) {
        showNotification("Пожалуйста, перезагрузите страницу или попробуйте позже", "error", 5000)
        throw new Error("Page is destroyed. Admins sidebar elements not found")
    }
    const user = JSON.parse(localStorage.getItem('user'))
    adminAvatar.textContent = user.name.toUpperCase().slice(0, 2);
    adminName.textContent = user.name
    adminEmail.textContent = user.email
});