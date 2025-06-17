import TableComponent from '../components/TableComponent.js';
import EntityModal from '../components/EntityModal.js';
import EntitySelectField from '../components/EntitySelectField.js';

document.addEventListener('DOMContentLoaded', () => {
    const apiEndpoint = '/products-import';
    const tableContainerId = 'tableContainer';
    const addEntityBtnId = 'addEntityBtn';

    const productsColumnDefinitions = [
        {label: 'Тип', field: 'product_type.name', sortable: true, render: (productImport) => productImport.product_type?.name || '-'},
        {label: 'Название', field: 'name', sortable: true, render: (productImport) => productImport.name},
        {label: 'Артикул', field: 'article', sortable: true, render: (productImport) => productImport.article},
        {label: 'Минимальная стоимость', field: 'product_type.name', sortable: true, render: (productImport) => productImport.minimum_cost},
    ];

    const productTypeSelectField = new EntitySelectField({
        id: 'product_type_select',
        name: 'type_id',
        label: 'Тип',
        apiEndpoint: '/products-types',
        formatItem: (product_type) => product_type.name,
        required: false,
        placeholder: 'Выберите тип...'
    });

    const productsImportFieldDefinitions = [
        {name: 'name', label: 'Название', type: 'textarea', required: true},
        {name: 'article', label: 'Артикул', type: 'text', required: true},
        {name: 'minimum_cost', label: 'Мин. цена', type: 'float', required: true},
        {
            name: 'type_id',
            type: 'custom',
            componentInstance: productTypeSelectField,
            render: () => productTypeSelectField.getElement().outerHTML,
            getValue: () => productTypeSelectField.getValue(),
            setValue: (value) => productTypeSelectField.setValue(value)
        },
    ];

    const productsImportModal = new EntityModal({
        modalId: 'productsImportModal',
        apiEndpoint: apiEndpoint,
        fieldDefinitions: productsImportFieldDefinitions,
        titleNew: 'Добавить продукт',
        titleEdit: 'Редактировать продукт',
        onSaveSuccess: (action) => {
            if (action === "create") {
                showNotification("Продукт успешно добавлен!", "success");
            } else if (action === "update") {
                showNotification("Продукт успешно обновлён!", "success");
            } else if (action === "delete") {
                showNotification("Продукт успешно удалён!", "success");
            }
            productsTable.loadData();
        },
    });

    const productsTable = new TableComponent({
        apiEndpoint: apiEndpoint,
        containerId: tableContainerId,
        columnDefinitions: productsColumnDefinitions,
        onEdit: (id) => productsImportModal.show(id),
        onDelete: async () => {
            try {
                await productsImportModal.deleteEntity();
                return true;
            } catch (error) {
                return false;
            }
        }
    });

    const addEntityButton = document.getElementById(addEntityBtnId);
    if (addEntityButton) {
        addEntityButton.addEventListener('click', () => productsImportModal.show());
    }
});