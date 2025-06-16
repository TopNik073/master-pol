import api from '../api.js';
import { ConfirmModal } from './ConfirmModal.js';

class EntityModal {
    /**
     * @param {Object} options
     * @param {string} options.modalId - ID модального окна (например, 'userModal')
     * @param {string} options.apiEndpoint - Базовый URL для API сущности (например, '/users')
     * @param {Array<Object>} options.fieldDefinitions - Массив объектов, описывающих поля формы
     *   Пример: [{ name: 'name', label: 'Имя', type: 'text', required: true }, { name: 'role', label: 'Роль', type: 'select', options: [{value: 'admin', text: 'Администратор'}] }]
     * @param {Function} [options.onSaveSuccess] - Callback-функция, вызываемая после успешного сохранения/удаления
     * @param {string} [options.titleNew='Добавить запись'] - Заголовок для нового элемента
     * @param {string} [options.titleEdit='Редактировать запись'] - Заголовок для редактирования элемента
     */
    constructor({ modalId, apiEndpoint, fieldDefinitions, onSaveSuccess, titleNew = 'Добавить запись', titleEdit = 'Редактировать запись' }) {
        this.modalId = modalId;
        this.apiEndpoint = apiEndpoint;
        this.fieldDefinitions = fieldDefinitions;
        this.onSaveSuccess = onSaveSuccess;
        this.titleNew = titleNew;
        this.titleEdit = titleEdit;

        this.entityId = null;
        this.modalElement = null;
        this.modalTitleElement = null;
        this.formElement = null;
        this.saveButton = null;
        this.deleteButton = null;

        this.data = null;

        this.confirmModal = new ConfirmModal();

        this.initModal();
    }

    initModal() {
        const modalHtml = `
            <div class="modal fade" id="${this.modalId}" tabindex="-1" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="${this.modalId}Label">${this.titleNew}</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <form id="${this.modalId}Form">
                                ${this.generateFormFields()}
                            </form>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="button button-secondary me-auto d-none" style="background-color: var(--red); color: var(--admin-sidebar-color);" id="${this.modalId}DeleteBtn"><i class="fas fa-trash"></i> Удалить</button>
                            <button type="button" class="button button-secondary" data-bs-dismiss="modal">Отмена</button>
                            <button type="submit" class="button button-primary" form="${this.modalId}Form" id="${this.modalId}SaveBtn">Сохранить</button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', modalHtml);
        this.modalElement = document.getElementById(this.modalId);
        this.modalTitleElement = document.getElementById(`${this.modalId}Label`);
        this.formElement = document.getElementById(`${this.modalId}Form`);
        this.saveButton = document.getElementById(`${this.modalId}SaveBtn`);
        this.deleteButton = document.getElementById(`${this.modalId}DeleteBtn`);

        this.attachEventListeners();
        this.renderCustomComponents();
    }

    generateFormFields() {
        return this.fieldDefinitions.map(field => {
            if (field.type === 'custom') {
                return `
                    <div class="mb-3" id="custom-field-container-${field.name}">
                        <label for="${field.name}" class="form-label">${field.label}</label>
                        <!-- Custom component will be rendered here -->
                    </div>
                `;
            }

            let inputHtml = '';
            const baseClasses = field.type === 'select' ? 'form-select' : 
                               field.type === 'checkbox' ? 'form-check-input' : 'form-control';
            const focusClass = 'focus-green';
            
            switch (field.type) {
                case 'text':
                case 'email':
                case 'password':
                case 'number':
                    inputHtml = `<input type="${field.type}" class="${baseClasses} ${focusClass}" id="${field.name}" ${field.required ? 'required' : ''}>`;
                    break;

                case 'float':
                    inputHtml = `<input type="number" step="0.01" class="${baseClasses} ${focusClass}" id="${field.name}" ${field.required ? 'required' : ''}>`;
                    break;

                case 'textarea':
                    inputHtml = `<textarea class="${baseClasses} ${focusClass}" id="${field.name}" rows="3" ${field.required ? 'required' : ''}></textarea>`;
                    break;

                case 'select':
                    inputHtml = `<select class="${baseClasses} ${focusClass}" id="${field.name}" ${field.required ? 'required' : ''}>
                                 <option value="">Выберите...</option>
                                 ${field.options ? field.options.map(option => `<option value="${option.value}">${option.text}</option>`).join('') : ''}
                             </select>`;
                    break;

                case 'checkbox':
                    inputHtml = `<div class="form-check">
                                 <input class="${baseClasses} ${focusClass}" type="checkbox" id="${field.name}">
                                 <label class="form-check-label" for="${field.name}">${field.label}</label>
                             </div>`;
                    return inputHtml;

                case 'datetime':
                    inputHtml = `<input type="datetime-local" class="${baseClasses} ${focusClass}" id="${field.name}" ${field.required ? 'required' : ''}>`;
                    break;

                case 'date':
                    inputHtml = `<input type="date" class="${baseClasses} ${focusClass}" id="${field.name}" ${field.required ? 'required' : ''}>`;
                    break;

                default:
                    inputHtml = `<input type="text" class="${baseClasses} ${focusClass}" id="${field.name}" ${field.required ? 'required' : ''}>`;
            }
            
            return `
                <div class="mb-3">
                    <label for="${field.name}" class="form-label">${field.label}</label>
                    ${inputHtml}
                </div>
            `;
        }).join('');
    }

    renderCustomComponents() {
        this.fieldDefinitions.forEach(field => {
            if (field.type === 'custom' && field.componentInstance) {
                const container = document.getElementById(`custom-field-container-${field.name}`);
                if (container) {
                    const existingLabel = container.querySelector('label');
                    if (existingLabel && field.componentInstance.getElement().querySelector('label')) {
                        existingLabel.remove();
                    }
                    container.appendChild(field.componentInstance.getElement());
                }
            }
        });
    }

    /**
     * Открывает модальное окно для создания или редактирования сущности
     * @param {string|null} entityId - ID сущности для редактирования, или null для создания
     */
    async show(entityId = null) {
        this.entityId = entityId;
        this.resetForm();

        if (this.entityId) {
            this.modalTitleElement.textContent = this.titleEdit;
            this.deleteButton.classList.remove('d-none');
            await this.loadEntityData(this.entityId);
        } else {
            this.modalTitleElement.textContent = this.titleNew;
            this.deleteButton.classList.add('d-none');
        }

        const modalInstance = new bootstrap.Modal(this.modalElement);
        modalInstance.show();

        // Initialize Flatpickr for all date/datetime fields after data is loaded/cleared
        this.formElement.querySelectorAll('input[type="date"], input[type="datetime-local"]').forEach(input => {
            // Destroy existing instance if any, to ensure proper re-initialization
            if (input._flatpickr) {
                input._flatpickr.destroy();
            }

            let defaultDate = null;
            if (this.data && this.data[input.id]) {
                defaultDate = this.data[input.id];
            }
            
            flatpickr(input, {
                enableTime: input.type === 'datetime-local',
                dateFormat: input.type === 'datetime-local' ? 'Y-m-d H:i' : 'Y-m-d',
                time_24hr: true,
                locale: 'ru',
                defaultDate: defaultDate
            });
        });
    }

    async loadEntityData(id) {
        try {
            const response = await api.get(`${this.apiEndpoint}/${id}`);
            const data = response.data;
            this.data = data
            this.fillForm(data);
        } catch (error) {
            showNotification(error.message, "error");
            console.error(`Failed to load entity ${id}:`, error);
            const modalInstance = bootstrap.Modal.getInstance(this.modalElement);
            if (modalInstance) modalInstance.hide();
        }
    }

    fillForm(data) {
        this.fieldDefinitions.forEach(field => {
            if (field.type === 'custom' && field.componentInstance && field.componentInstance.setValue) {
                const valueToSet = data[field.dataKey || field.name];
                field.componentInstance.setValue(valueToSet);
            } else {
                const inputElement = document.getElementById(field.name);
                if (inputElement) {
                    if (field.type === 'checkbox') {
                        inputElement.checked = data[field.name];
                    } else if (field.type === 'date') {
                        inputElement.value = new Date(data[field.name]).toISOString().split('T')[0];
                    } else if (field.type === 'datetime') {
                        const date = new Date(data[field.name]);
                        const localDateTime = new Date(date.getTime() - date.getTimezoneOffset() * 60000).toISOString().slice(0, 16);
                        inputElement.value = localDateTime;
                    } else if (field.type === 'float') {
                        inputElement.value = field.formatValue ? field.formatValue(data[field.name]) : (parseFloat(data[field.name]) || 0.0);
                    } else if (field.type === 'number') {
                        inputElement.value = parseInt(data[field.name]) || 0;
                    } else if (field.type === 'select') {
                        inputElement.value = data[field.name] || '';
                    } else{
                        inputElement.value = data[field.name] || '';
                    }
                }
            }
        });
    }

    resetForm() {
        // Destroy existing Flatpickr instances before resetting the form
        this.formElement.querySelectorAll('input[type="date"], input[type="datetime-local"]').forEach(input => {
            if (input._flatpickr) {
                input._flatpickr.destroy();
            }
        });

        this.formElement.reset();
        this.data = null; // Clear any loaded data
        this.fieldDefinitions.forEach(field => {
            if (field.type === 'custom' && field.componentInstance && field.componentInstance.clearSelection) {
                field.componentInstance.clearSelection();
            } else {
                const inputElement = document.getElementById(field.name);
                if (inputElement) {
                    if (field.type === 'checkbox') {
                        inputElement.checked = false;
                    } else if (field.type === 'float') {
                        inputElement.value = 0.0;
                    } else if (field.type === 'number') {
                        inputElement.value = 0;
                    } else if (field.type === 'select') {
                        inputElement.value = '';
                    } else{
                        // For date/datetime, input.value is cleared by formElement.reset() and defaultDate will be set by Flatpickr
                        // For other types, this will clear the value
                        if (field.type !== 'date' && field.type !== 'datetime') {
                             inputElement.value = '';
                        }
                    }
                }
            }
        });
    }

    attachEventListeners() {
        this.formElement.addEventListener('submit', (e) => {
            e.preventDefault();
            this.saveEntity();
        });

        this.deleteButton.addEventListener('click', () => this.deleteEntity());

        this.modalElement.addEventListener('hidden.bs.modal', () => {
            this.resetForm();
        });
    }

    async saveEntity() {
        const formData = {};
    this.fieldDefinitions.forEach(field => {
        if (field.type === 'custom' && field.getValue) {
            formData[field.name] = field.getValue();
        } else {
            const inputElement = document.getElementById(field.name);
            if (inputElement) {
                if (field.formatBeforeRequest) {
                    formData[field.name] = field.formatBeforeRequest(inputElement.value);
                    return;
                };
                if (field.type === 'checkbox') {
                    formData[field.name] = inputElement.checked;
                } else if (field.type === 'number') {
                    formData[field.name] = parseFloat(inputElement.value);
                } else {
                    formData[field.name] = inputElement.value;
                    console.log(field.name, inputElement.value, typeof(inputElement.value))
                }
            }
        }
    });

        try {
            let response;
            if (this.entityId) {
                // For PUT request, include ID in data or route
                response = await api.put(`${this.apiEndpoint}/${this.entityId}`, formData);
                if (this.onSaveSuccess) {
                    this.onSaveSuccess("update");
                }
            } else {
                response = await api.post(this.apiEndpoint, formData);
                if (this.onSaveSuccess) {
                    this.onSaveSuccess("create");
                }
            }

            const modalInstance = bootstrap.Modal.getInstance(this.modalElement);
            if (modalInstance) modalInstance.hide();

        } catch (error) {
            showNotification(error.message, "error");
            console.error('Failed to save entity:', error);
        }
    }

    async deleteEntity() {
        const modalInstance = bootstrap.Modal.getInstance(this.modalElement);
        if (modalInstance) modalInstance.hide();
        const confirmed = await this.confirmModal.show();
        if (!confirmed) {
            if (modalInstance) {
                this.fillForm(this.data);
                modalInstance.show();
                return;
            }
        }

        try {
            await api.delete(`${this.apiEndpoint}/${this.entityId}`);

            if (this.onSaveSuccess) {
                this.onSaveSuccess("delete");
            }

        } catch (error) {
            // showNotification(error.message, "error");
            console.error('Failed to delete entity:', error);
        }
    }
}

export default EntityModal; 