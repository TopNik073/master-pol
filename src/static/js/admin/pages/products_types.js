import TableComponent from '../components/TableComponent.js';
import EntityModal from '../components/EntityModal.js';

document.addEventListener('DOMContentLoaded', () => {
    const apiEndpoint = '/products-types';
    const tableContainerId = 'tableContainer';
    const addEntityBtnId = 'addEntityBtn';

    const productsTypesColumnDefinitions = [
        {label: 'Название типа', field: 'name', sortable: true, render: (productType) => productType.name},
        {label: 'Коэффициент', field: 'coefficient', sortable: true, render: (productType) => productType.coefficient},
    ];


    const productsTypesFieldDefinitions = [
        {name: 'name', label: 'Название', type: 'text', required: true},
        {name: 'coefficient', label: 'Коэффициент', type: 'float', required: true}
    ];

    const productTypesModal = new EntityModal({
        modalId: 'productTypesModal',
        apiEndpoint: apiEndpoint,
        fieldDefinitions: productsTypesFieldDefinitions,
        titleNew: 'Добавить тип',
        titleEdit: 'Редактировать тип',
        onSaveSuccess: (action) => {
            if (action === "create") {
                showNotification("Тип успешно добавлен!", "success");
            } else if (action === "update") {
                showNotification("Тип успешно обновлён!", "success");
            } else if (action === "delete") {
                showNotification("Тип успешно удалён!", "success");
            }
            productsTable.loadData();
        },
    });

    const productsTable = new TableComponent({
        apiEndpoint: apiEndpoint,
        containerId: tableContainerId,
        columnDefinitions: productsTypesColumnDefinitions,
        onEdit: (id) => productTypesModal.show(id),
        onDelete: async () => {
            try {
                await productTypesModal.deleteEntity();
                return true;
            } catch (error) {
                return false;
            }
        }
    });

    const addEntityButton = document.getElementById(addEntityBtnId);
    if (addEntityButton) {
        addEntityButton.addEventListener('click', () => productTypesModal.show());
    }
});