import TableComponent from '../components/TableComponent.js';
import EntityModal from '../components/EntityModal.js';

document.addEventListener('DOMContentLoaded', () => {
    const apiEndpoint = '/partners-bid';
    const tableContainerId = 'tableContainer';
    const addEntityBtnId = 'addEntityBtn';

    const partnersBidColumnDefinitions = [
        {label: 'Тип партнёра', field: 'partner_type', sortable: true, render: (partner) => partner.partner_type},
        {label: 'Название партнёра', field: 'name', sortable: true, render: (partner) => partner.name},
        {label: 'e-mail', field: 'email', sortable: true, render: (partner) => partner.email},
        {label: 'Юр. адрес', field: 'ur_address', sortable: true, render: (partner) => partner.ur_address},
        {label: 'Директор', field: 'director', sortable: true, render: (partner) => partner.director},
        {label: 'Номер тел.', field: 'phone_nummber', sortable: true, render: (partner) => partner.phone_number},
        {label: 'ИНН', field: 'inn', sortable: false, render: (partner) => partner.inn},
    ]

    const partnersBidFieldDefinitions = [
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

    const partnerBidModal = new EntityModal({
        modalId: 'partnerBidModal',
        apiEndpoint: apiEndpoint,
        fieldDefinitions: partnersBidFieldDefinitions,
        titleNew: 'Добавить партнёра',
        titleEdit: 'Редактировать партнёра',
        onSaveSuccess: (action) => {
            if (action === "update") {
                showNotification("Статус заявки обновлён!", "success");
            } else if (action === "delete") {
                showNotification("Заявка отклонена!", "success");
            }
            partnersBidTable.loadData(); // Reload table data after save
        },
    })

    const partnersBidTable = new TableComponent({
        apiEndpoint: apiEndpoint,
        containerId: tableContainerId,
        columnDefinitions: partnersBidColumnDefinitions,
        onEdit: (id) => partnerBidModal.show(id),
        onDelete: async () => {
            try {
                await partnerBidModal.deleteEntity();
                return true;
            } catch (error) {
                return false;
            }
        }
    });

    const addEntityButton = document.getElementById(addEntityBtnId);
    if (addEntityButton) {
        addEntityButton.addEventListener('click', () => partnerBidModal.show());
    }
});