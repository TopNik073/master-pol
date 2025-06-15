import TableComponent from '../components/TableComponent.js';
import EntityModal from '../components/EntityModal.js';

document.addEventListener('DOMContentLoaded', () => {
    const apiEndpoint = '/users';
    const tableContainerId = 'tableContainer';
    const addEntityBtnId = 'addEntityBtn';

    // Column definitions for the Users table
    const userColumnDefinitions = [
        { label: 'Имя', field: 'name', sortable: true, render: (user) => user.name },
        { label: 'Email', field: 'email', sortable: true, render: (user) => user.email },
        { label: 'Роль', field: 'role', sortable: true, render: (user) => {
            if (user.role === "admin") {
                return `
                    <div style="font-weight: 700; color: var(--green-dark);">
                        Администратор
                    </div>
                    `
            } else {
                return "Пользователь"
            }
        } },
    ];

    // Field definitions for the User modal (Add/Edit)
    const userFieldDefinitions = [
        { name: 'name', label: 'Имя', type: 'text', required: true },
        { name: 'email', label: 'Email', type: 'email', required: true },
        { name: 'password', label: 'Пароль', type: 'password', required: false },
        { 
            name: 'role', 
            label: 'Роль', 
            type: 'select', 
            required: true, 
            options: [
                { value: 'admin', text: 'Администратор' },
                { value: 'user', text: 'Пользователь' },
            ]
        },
    ];

    const userModal = new EntityModal({
        modalId: 'userModal',
        apiEndpoint: apiEndpoint,
        fieldDefinitions: userFieldDefinitions,
        titleNew: 'Добавить пользователя',
        titleEdit: 'Редактировать пользователя',
        onSaveSuccess: (action) => {
            if (action === "create") {
                showNotification("Пользователь успешно создан!", "success");
            } else if (action === "update") {
                showNotification("Пользователь успешно обновлён!", "success");
            } else if (action === "delete") {
                showNotification("Пользователь успешно удалён!", "success");
            }
            userTable.loadData(); // Reload table data after save
        },
    });

    const userTable = new TableComponent({
        apiEndpoint: apiEndpoint,
        containerId: tableContainerId,
        columnDefinitions: userColumnDefinitions,
        onEdit: (id) => userModal.show(id), // Open modal in edit mode
        onDelete: async () => {
            try {
                await userModal.deleteEntity();
                return true; // Indicate successful deletion for TableComponent to reload
            } catch (error) {
                return false; // Indicate failed deletion
            }
        }
    });

    // Event listener for the 'Add User' button
    const addEntityButton = document.getElementById(addEntityBtnId);
    if (addEntityButton) {
        addEntityButton.addEventListener('click', () => userModal.show()); // Open modal in add mode
    }
}); 