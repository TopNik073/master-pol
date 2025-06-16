document.getElementById('profileForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const formData = {
        name: document.getElementById('userName').value,
        email: document.getElementById('userEmail').value,
    };
    const userPassword = document.getElementById('userPassword').value;
    if (userPassword) {
        formData.password = userPassword;
    };

    try {
        const response = await axios.put(`/users/me`, formData);

        if (response.status !== 200) {
            showNotification('Попробуйте позже :(', 'error', 10000);
        }

        localStorage.setItem('user', JSON.stringify(response.data.data));
        closeModal('profileModal');

        showNotification('Профиль успешно изменён', 'success', 10000);


        } catch (error) {
            showNotification(error.message, 'error');
        };
});