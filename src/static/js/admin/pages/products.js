import TableComponent from '../components/TableComponent.js';
import EntityModal from '../components/EntityModal.js';
import EntitySelectField from '../components/EntitySelectField.js';

document.addEventListener('DOMContentLoaded', () => {
    const apiEndpoint = '/products';
    const tableContainerId = 'tableContainer';
    const addEntityBtnId = 'addEntityBtn';

    const productsColumnDefinitions = [
        {label: 'Продукт', field: 'product_import.name', sortable: true, render: (product) => product.product_import.name},
        {label: 'Кол-во проданной продукции', sortable: true, field: 'quantity_products', render: (product) => product.quantity_products},
        {label: 'Партнёр', field: 'partner.name', sortable: true, render: (product) => product.partner?.name || '-'},
        {label: 'Тип продукта', field: 'product_type.name', sortable: true, render: (product) => product.product_import.product_type?.name || '-'},
        {label: 'Дата продажи', field: 'sell_date', sortable: true, render: (product) => new Date(product.sell_date).toISOString().split('T')[0]},
    ];

    // Создаем экземпляры EntitySelectField для связанных сущностей
    const partnerSelectField = new EntitySelectField({
        id: 'partner_select',
        name: 'partner_id',
        label: 'Партнёр',
        apiEndpoint: '/partners',
        formatItem: (partner) => partner.name,
        required: true,
        placeholder: 'Выберите партнёра...'
    });

    const productImportSelectField = new EntitySelectField({
        id: 'product_import_select',
        name: 'product_import_id',
        label: 'Продукт',
        apiEndpoint: '/products-import',
        formatItem: (product_import) => product_import.name,
        required: true,
        placeholder: 'Выберите продукт...'
    });

    const productsFieldDefinitions = [
        {
            name: 'partner_id',
            dataKey: 'partner',
            type: 'custom',
            componentInstance: partnerSelectField,
            render: () => partnerSelectField.getElement().outerHTML,
            getValue: () => partnerSelectField.getValue(),
            setValue: (value) => partnerSelectField.setValue(value)
        },
        {
            name: 'product_import_id',
            dataKey: 'product_import',
            type: 'custom',
            componentInstance: productImportSelectField,
            render: () => productImportSelectField.getElement().outerHTML,
            getValue: () => productImportSelectField.getValue(),
            setValue: (value) => productImportSelectField.setValue(value)
        },
        {name: 'quantity_products', label: 'Кол-во продукции', type: 'number', required: true},
        {name: 'sell_date', label: 'Дата продажи', type: 'date', required: true}
    ];

    const productModal = new EntityModal({
        modalId: 'productModal',
        apiEndpoint: apiEndpoint,
        fieldDefinitions: productsFieldDefinitions,
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
        onEdit: (id) => productModal.show(id),
        onDelete: async () => {
            try {
                await productModal.deleteEntity();
                return true;
            } catch (error) {
                return false;
            }
        }
    });

    const addEntityButton = document.getElementById(addEntityBtnId);
    if (addEntityButton) {
        addEntityButton.addEventListener('click', () => productModal.show());
    }
});