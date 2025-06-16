import TableComponent from '../components/TableComponent.js';
import EntityModal from '../components/EntityModal.js';

document.addEventListener('DOMContentLoaded', () => {
    const apiEndpoint = '/materials';
    const tableContainerId = 'tableContainer';
    const addEntityBtnId = 'addEntityBtn';

    // Column definitions for the Users table
    const materialsColumnDefinitions = [
        { label: 'Название', field: 'name', sortable: true, render: (material) => material.name },
        { label: 'Процент брака', field: 'defect_rate_percent', sortable: true, render: (material) => `${parseFloat(material.defect_rate_percent) * 100} %` }
    ];

    // Field definitions for the User modal (Add/Edit)
    const materialsFieldDefinitions = [
        { name: 'name', label: 'Название материала', type: 'text', required: true },
        { name: 'defect_rate_percent', label: 'Процент брака', type: 'float', required: true, 
            formatBeforeRequest: (value) => parseFloat(value) / 100,
            formatValue: (value) => parseFloat(value) * 100 }
    ];

    const materialsModal = new EntityModal({
        modalId: 'materialsModal',
        apiEndpoint: apiEndpoint,
        fieldDefinitions: materialsFieldDefinitions,
        titleNew: 'Добавить материал',
        titleEdit: 'Редактировать материал',
        onSaveSuccess: (action) => {
            if (action === "create") {
                showNotification("Материал успешно создан!", "success");
            } else if (action === "update") {
                showNotification("Материал успешно обновлён!", "success");
            } else if (action === "delete") {
                showNotification("Материал успешно удалён!", "success");
            }
            materialsTable.loadData(); // Reload table data after save
        },
    });

    const materialsTable = new TableComponent({
        apiEndpoint: apiEndpoint,
        containerId: tableContainerId,
        columnDefinitions: materialsColumnDefinitions,
        onEdit: (id) => materialsModal.show(id), // Open modal in edit mode
        onDelete: async () => {
            try {
                await materialsModal.deleteEntity();
                return true; // Indicate successful deletion for TableComponent to reload
            } catch (error) {
                return false; // Indicate failed deletion
            }
        }
    });

    // Event listener for the 'Add User' button
    const addEntityButton = document.getElementById(addEntityBtnId);
    if (addEntityButton) {
        addEntityButton.addEventListener('click', () => materialsModal.show()); // Open modal in add mode
    }
}); 