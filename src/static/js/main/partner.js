document.getElementById('partnerForm').addEventListener('submit', async function(e) {
        e.preventDefault();

        const formData = {
            partner_type: document.getElementById('partnerType').value,
            name: document.getElementById('name').value,
            email: document.getElementById('email').value,
            ur_address: document.getElementById('urAddress').value,
            director: document.getElementById('director').value,
            phone_number: document.getElementById('phoneNumber').value,
            inn: document.getElementById('inn').value
        };

        try {
            const defAxiosUrl = axios.defaults.baseURL
            axios.defaults.baseURL = ''
            const response = await axios.post('api/admin/v1/partners-bid', formData)
            axios.defaults.baseURL = defAxiosUrl

            if (response.status !== 200) {
                showNotification('Ошибка при отправке заявки', 'error', 10000);
            }

            // Close modal
            closeModal('partnerModal');

            // Show success notification
            showNotification('Заявка успешно отправлена! Мы свяжемся с вами в ближайшее время.', 'success', 10000);


        } catch (error) {
            showNotification(error.message, 'error');
        }
    });
