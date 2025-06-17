import api from '../api.js';

class TableComponent {
    /**
     * @param {Object} options
     * @param {string} options.apiEndpoint - Базовый URL для API сущности (например, '/users')
     * @param {string} options.containerId - ID HTML-элемента, куда будет рендериться таблица
     * @param {Array<Object>} options.columnDefinitions - Массив объектов, описывающих столбцы таблицы
     * @param {number} [options.initialPerPage=10] - Начальное количество элементов на странице
     * @param {Function} [options.onEdit] - Callback-функция для редактирования (принимает ID)
     * @param {Function} [options.onDelete] - Callback-функция для удаления (принимает ID)
     * @param {string} [options.searchInputElementId='searchInput'] - ID поля ввода для поиска
     */
    constructor({ apiEndpoint, containerId, columnDefinitions, initialPerPage = 10, onEdit, onDelete, searchInputElementId = 'searchInput' }) {
        this.apiEndpoint = apiEndpoint;
        this.container = document.getElementById(containerId);
        this.columnDefinitions = columnDefinitions;
        this.currentPage = 1;
        this.perPage = initialPerPage;
        this.searchQuery = '';
        this.orderBy = null;
        this.orderDirection = 'asc';
        this.onEdit = onEdit;
        this.onDelete = onDelete;
        this.searchInputElement = document.getElementById(searchInputElementId);

        this.init();
    }

    async init() {
        this.renderBaseTable();
        await this.loadData();
        this.attachEventListeners();
    }

    renderBaseTable() {
        this.container.innerHTML = `
            <div class="table-responsive">
                <table class="table table-hover table-striped">
                    <thead>
                        <tr>
                            ${this.columnDefinitions.map(col => `
                                <th class="${col.sortable ? 'sortable' : ''}" data-sort="${col.field || ''}">${col.label}</th>
                            `).join('')}
                            <th class="text-end">Действия</th>
                        </tr>
                    </thead>
                    <tbody id="tableBody"></tbody>
                </table>
            </div>
            <div id="paginationControls" class="d-flex justify-content-end mt-3"></div>
        `;
    }

    async loadData() {
        try {
            const response = await api.get(this.apiEndpoint, {
                page: this.currentPage,
                per_page: this.perPage,
                search_query: this.searchQuery,
                order_by: this.orderBy,
                order_direction: this.orderDirection
            });
            this.renderRows(response.data.items);
            this.renderPagination(response.data.meta.total);
        } catch (error) {
            console.error(`Failed to load data for ${this.apiEndpoint}:`, error);
            this.renderError(error.message);
        }
    }

    renderRows(items) {
    console.log(items)
        const tableBody = document.getElementById('tableBody');
        if (!tableBody) return;

        if (!items || items.length === 0) {
            tableBody.innerHTML = `<tr><td colspan="${this.columnDefinitions.length + 1}" class="text-center py-4">Нет данных</td></tr>`;
            return;
        }

        tableBody.innerHTML = items.map(item => {
            const cells = this.columnDefinitions.map(col => {
                const value = col.render ? col.render(item) : item[col.field];
                return `<td>${value || '-'}</td>`;
            }).join('');
            
            const actions = `
                <td class="text-end">
                    <button class="btn btn-sm btn-outline-primary me-2 edit-btn" data-id="${item.id}">
                        <i class="fas fa-edit"></i>
                        <span class="btn-text">Изменить</span>
                    </button>
                </td>
            `;
            return `<tr>${cells}${actions}</tr>`;
        }).join('');
    }

    renderPagination(total) {
        const totalPages = Math.ceil(total / this.perPage);
        const paginationControls = document.getElementById('paginationControls');
        if (!paginationControls) return;

        let html = '<ul class="pagination pagination-sm">';

        // Previous button
        html += `<li class="page-item ${this.currentPage === 1 ? 'disabled' : ''}">
                    <a class="page-link" href="#" data-page="${this.currentPage - 1}">Назад</a>
                </li>`;

        // Page numbers
        const maxPagesToShow = 5; // Limit to 5 page numbers
        let startPage = Math.max(1, this.currentPage - Math.floor(maxPagesToShow / 2));
        let endPage = Math.min(totalPages, startPage + maxPagesToShow - 1);

        if (endPage - startPage + 1 < maxPagesToShow) {
            startPage = Math.max(1, endPage - maxPagesToShow + 1);
        }

        for (let i = startPage; i <= endPage; i++) {
            html += `<li class="page-item ${this.currentPage === i ? 'active' : ''}">
                        <a class="page-link" href="#" data-page="${i}">${i}</a>
                    </li>`;
        }

        // Next button
        html += `<li class="page-item ${this.currentPage === totalPages ? 'disabled' : ''}">
                    <a class="page-link" href="#" data-page="${this.currentPage + 1}">Вперед</a>
                </li>`;

        html += '</ul>';
        paginationControls.innerHTML = html;
    }

    attachEventListeners() {
        // Search input
        if (this.searchInputElement) {
            let searchTimeout;
            this.searchInputElement.addEventListener('input', (e) => {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {
                    this.searchQuery = e.target.value;
                    this.currentPage = 1;
                    this.loadData();
                }, 500);
            });
        }

        // Column sorting
        this.container.addEventListener('click', (e) => {
            const th = e.target.closest('th.sortable');
            if (th) {
                const sortField = th.dataset.sort;
                if (this.orderBy === sortField) {
                    this.orderDirection = this.orderDirection === 'asc' ? 'desc' : 'asc';
                } else {
                    this.orderBy = sortField;
                    this.orderDirection = 'asc'; // Default to asc for new sort field
                }
                this.loadData();
            }
        });

        // Pagination clicks
        this.container.addEventListener('click', (e) => {
            const pageLink = e.target.closest('.page-link');
            if (pageLink && !pageLink.closest('.page-item').classList.contains('disabled')) {
                e.preventDefault();
                const page = parseInt(pageLink.dataset.page);
                if (page && page !== this.currentPage) {
                    this.currentPage = page;
                    this.loadData();
                }
            }
        });

        // Edit/Delete buttons
        this.container.addEventListener('click', async (e) => {
            const editBtn = e.target.closest('.edit-btn');
            
            if (editBtn) {
                const id = editBtn.dataset.id;
                if (this.onEdit) {
                    this.onEdit(id);
                }
            }
        });
    }

    renderError(message) {
        const tableBody = document.getElementById('tableBody');
        if (tableBody) {
            tableBody.innerHTML = `<tr><td colspan="${this.columnDefinitions.length + 1}" class="text-center py-4"><div class="alert alert-danger mb-0">Ошибка загрузки данных: ${message}</div></td></tr>`;
        }
        const paginationControls = document.getElementById('paginationControls');
        if (paginationControls) {
            paginationControls.innerHTML = '';
        }
    }
}

export default TableComponent; 