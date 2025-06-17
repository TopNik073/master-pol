import TableComponent from '../components/TableComponent.js';
import EntityModal from '../components/EntityModal.js';

document.addEventListener('DOMContentLoaded', () => {
    const apiEndpoint = '/partners';
    const tableContainerId = 'tableContainer';
    const addEntityBtnId = 'addEntityBtn';

    const partnersColumnDefinitions = [
        {label: 'Тип партнёра', field: 'partner_type', sortable: true, render: (partner) => partner.partner_type},
        {label: 'Название партнёра', field: 'name', sortable: true, render: (partner) => partner.name},
        {label: 'e-mail', field: 'email', sortable: true, render: (partner) => partner.email},
        // {label: 'Юр. адрес', field: 'ur_address', sortable: true, render: (partner) => partner.ur_address},
        // {label: 'Директор', field: 'director', sortable: true, render: (partner) => partner.director},
        // {label: 'Номер тел.', field: 'phone_nummber', sortable: true, render: (partner) => partner.phone_number},
        // {label: 'ИНН', field: 'inn', sortable: false, render: (partner) => partner.inn},
        {label: 'Рейтинг', field: 'rate', sortable: false, render: (partner) => partner.rate},
        {label: 'Скидка', field: 'discount', sortable: false, render: (partner) => `${parseInt(parseFloat(partner.discount) * 100)} %`},
        {label: 'Кол-во продукции', field: 'products', sortable: false, render: (partner) => partner.products.length},
        {label: 'Кол-во типов', field: 'products.product_type', sortable: false, render: (partner) => {
            if (partner.products.length === 0) return 0
            let prod_types = new Set()
            for (const prod of partner.products) {
                const type_id = prod.product_import?.product_type?.id
                if (!type_id) continue
                prod_types.add(type_id)
            }
            console.log(prod_types)
            return prod_types.size
        }}
    ]

    const partnersFieldDefinitions = [
        {name: 'partner_type', label: 'Тип партнёра', type: 'text', requierd: true},
        {name: 'name', label: 'Название партнёра', type: 'text', requierd: true},
        {name: 'email', label: 'e-mail', type: 'text', requierd: true},
        {name: 'ur_address', label: 'Юр. адрес', type: 'textarea', required: true},
        {name: 'director', label: 'Директор', type: 'text', required: true},
        {name: 'phone_number', label: 'Номер тел.', type: 'text', requierd: true},
        {name: 'inn', label: 'ИНН', type: 'number', required: true},
        {name: 'rate', label: 'Рейтинг', type: 'float', required: true},
        {name: 'status', label: 'Статус', type: 'select', requierd: true, options: [
            {value: 'active', text: 'В работе'},
            {value: 'pending', text: 'На рассмотрении'}
        ]}
    ]

    const partnerModal = new EntityModal({
        modalId: 'partnerModal',
        apiEndpoint: apiEndpoint,
        fieldDefinitions: partnersFieldDefinitions,
        titleNew: 'Добавить партнёра',
        titleEdit: 'Редактировать партнёра',
        onSaveSuccess: (action) => {
            if (action === "create") {
                showNotification("Партнёр успешно создан!", "success");
            } else if (action === "update") {
                showNotification("Партнёр успешно обновлён!", "success");
            } else if (action === "delete") {
                showNotification("Партнёр успешно удалён!", "success");
            }
            partnersTable.loadData(); // Reload table data after save
        },
    })

    const partnersTable = new TableComponent({
        apiEndpoint: apiEndpoint,
        containerId: tableContainerId,
        columnDefinitions: partnersColumnDefinitions,
        onEdit: (id) => partnerModal.show(id),
        onDelete: async () => {
            try {
                await partnerModal.deleteEntity();
                return true;
            } catch (error) {
                return false;
            }
        }
    });

    const addEntityButton = document.getElementById(addEntityBtnId);
    if (addEntityButton) {
        addEntityButton.addEventListener('click', () => partnerModal.show());
    }
});