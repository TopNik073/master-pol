import api from '../api.js';

class EntitySelectField {
    constructor(options) {
        this.options = options;
        this.id = options.id;
        this.name = options.name;
        this.label = options.label;
        this.apiEndpoint = options.apiEndpoint;
        this.formatItem = options.formatItem || ((item) => item.name);
        this.required = options.required || false;
        this.placeholder = options.placeholder || 'Выберите...';
        this.perPage = options.perPage || 10;
        this.searchQuery = '';
        this.currentPage = 1;
        this.totalItems = 0;
        this.selectedItem = null;
        this.items = [];
        this.dropdownVisible = false;

        this.initElements();
        this.attachEventListeners();
        
        // Загружаем начальные данные
        this.loadItems();
    }

    // Utility for debouncing function calls
    _debounce(func, delay) {
        let timeout;
        return function(...args) {
            const context = this;
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(context, args), delay);
        };
    }

    initElements() {
        this.element = document.createElement('div');
        this.element.className = 'mb-3 enhanced-entity-select-field';
        this.element.style.position = 'relative';

        const label = document.createElement('label');
        label.className = 'form-label';
        label.htmlFor = this.id;
        label.textContent = this.label;
        this.element.appendChild(label);

        this.inputGroup = document.createElement('div');
        this.inputGroup.className = 'input-group';

        this.searchInput = document.createElement('input');
        this.searchInput.type = 'text';
        this.searchInput.className = 'form-control focus-green';
        this.searchInput.id = this.id;
        this.searchInput.name = this.name;
        this.searchInput.placeholder = this.placeholder;
        this.searchInput.autocomplete = 'off';
        if (this.required) this.searchInput.required = true;
        this.inputGroup.appendChild(this.searchInput);

        this.hiddenInput = document.createElement('input');
        this.hiddenInput.type = 'hidden';
        this.hiddenInput.name = `${this.name}_id`;
        this.inputGroup.appendChild(this.hiddenInput);

        this.clearButton = document.createElement('button');
        this.clearButton.type = 'button';
        this.clearButton.className = 'btn btn-outline-secondary';
        this.clearButton.innerHTML = '<i class="fas fa-times"></i>';
        this.inputGroup.appendChild(this.clearButton);

        this.element.appendChild(this.inputGroup);

        this.dropdown = document.createElement('div');
        this.dropdown.className = 'dropdown-menu w-100';
        this.dropdown.style.display = 'none';
        this.dropdown.style.maxHeight = '250px';
        this.dropdown.style.overflowY = 'auto';
        this.dropdown.style.position = 'absolute';
        this.dropdown.style.zIndex = '1000';
        this.element.appendChild(this.dropdown);

        this.pagination = document.createElement('div');
        this.pagination.className = 'd-flex justify-content-between align-items-center p-2 border-top';
        this.pagination.style.display = 'none';

        this.prevBtn = document.createElement('button');
        this.prevBtn.className = 'btn btn-sm btn-outline-secondary prev-btn';
        this.prevBtn.textContent = 'Назад';
        this.pagination.appendChild(this.prevBtn);

        this.pageInfo = document.createElement('span');
        this.pageInfo.className = 'page-info';
        this.pagination.appendChild(this.pageInfo);

        this.nextBtn = document.createElement('button');
        this.nextBtn.className = 'btn btn-sm btn-outline-secondary next-btn';
        this.nextBtn.textContent = 'Вперед';
        this.pagination.appendChild(this.nextBtn);

        this.dropdown.appendChild(this.pagination);
    }

    attachEventListeners() {
        this.searchInput.addEventListener('input', this._debounce((e) => {
            this.searchQuery = e.target.value;
            this.currentPage = 1;
            this.loadItems();
        }, 500));

        this.searchInput.addEventListener('focus', () => {
            this.showDropdown();
            if (this.items.length === 0) {
                this.loadItems();
            }
        });

        document.addEventListener('click', (e) => {
            if (!this.element.contains(e.target)) {
                this.hideDropdown();
            }
        });

        this.clearButton.addEventListener('click', () => {
            this.clearSelection();
        });
    }

    showDropdown() {
        this.dropdown.style.display = 'block';
        this.dropdownVisible = true;
    }

    hideDropdown() {
        this.dropdown.style.display = 'none';
        this.dropdownVisible = false;
    }

    clearSelection() {
        this.searchInput.value = '';
        this.hiddenInput.value = '';
        this.selectedItem = null;
        this.hideDropdown();
    }

    async loadItems() {
        try {
            const response = await api.get(this.apiEndpoint,  {
                page: this.currentPage,
                per_page: this.perPage,
                search_query: this.searchQuery,
            });

            this.items = response.data.items || response.data;
            this.totalItems = response.data.total || response.data.length;

            this.renderItems();
            this.showDropdown();
        } catch (error) {
            console.error(`Failed to load items from ${this.apiEndpoint}:`, error);
            this.hideDropdown();
        }
    }

    renderItems() {
        while (this.dropdown.firstChild) {
            this.dropdown.removeChild(this.dropdown.firstChild);
        }

        if (this.items.length === 0) {
            const noResults = document.createElement('div');
            noResults.className = 'dropdown-item';
            noResults.textContent = 'Ничего не найдено';
            this.dropdown.appendChild(noResults);
        } else {
            this.items.forEach(item => {
                const itemElement = document.createElement('button');
                itemElement.type = 'button';
                itemElement.className = 'dropdown-item';
                itemElement.textContent = this.formatItem(item);
                itemElement.addEventListener('click', (e) => {
                    e.stopPropagation();
                    this.selectItem(item);
                });
                this.dropdown.appendChild(itemElement);
            });
        }
    }

    selectItem(item) {
        this.selectedItem = item;
        this.searchInput.value = this.formatItem(item);
        this.hiddenInput.value = item.id;
        this.hideDropdown();
    }

    getValue() {
        const value = this.hiddenInput.value;
        if (value === "") return null;
        return value
    }

    setValue(value) {
        console.log('EntitySelectField setValue called with:', value);
        
        if (!value) {
            console.log('No value provided, clearing selection');
            this.clearSelection();
            return;
        }

        // Если value это объект с id, используем его напрямую
        if (typeof value === 'object' && value.id) {
            console.log('Using provided object directly:', value);
            this.selectedItem = value;
            this.searchInput.value = this.formatItem(value);
            this.hiddenInput.value = value.id;
            return;
        }

        // Если value это ID, загружаем данные
        console.log('Loading data for ID:', value);
        api.get(`${this.apiEndpoint}/${value}`)
            .then(response => {
                console.log('Loaded data:', response.data);
                this.selectedItem = response.data;
                this.searchInput.value = this.formatItem(response.data);
                this.hiddenInput.value = response.data.id;
            })
            .catch(error => {
                console.error(`Failed to load item ${value}:`, error);
            });
    }

    getElement() {
        return this.element;
    }
}

export default EntitySelectField;