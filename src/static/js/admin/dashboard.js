import api from './api.js';

class Dashboard {
    constructor() {
        this.init();
    }

    async init() {
        const data = await this.get_stats()
        this.renderUI(data)
    }

    renderUI(data) {
        this.renderStats(data);
        this.renderSalesChart(data.weekly_sales);
        this.renderRecentSales(data.recent_sales_details);
    }

    async get_stats() {
        try {
            console.log('Loading dashboard data...');
            const response = await api.get('/stats');
            console.log('Received data:', response);
            
            if (!response.data) {
                throw new Error('No data received from API');
            }

            return response.data
        } catch (error) {
            console.error('Failed to load dashboard data:', error);
            this.showError(error);
        }
    }
    
    showError(error) {
        const recentSalesContainer = document.querySelector('#recentSalesContainer');
        if (recentSalesContainer) {
            recentSalesContainer.innerHTML = `
                <div class="text-center p-4">
                    <div class="mb-3" style="font-size: 3rem; color: #dc3545;">
                        <i class="bi bi-exclamation-triangle"></i>
                    </div>
                    <h3 class="h5 text-danger mb-2">Ошибка загрузки данных</h3>
                    <p class="text-muted small">${error.message}</p>
                    <button class="btn btn-sm mt-2 refresh-btn" style="background-color: #f4e8d3; color: #5a6d57;">
                        <i class="bi bi-arrow-clockwise me-1"></i> Повторить попытку
                    </button>
                </div>
            `;
            this.addRefreshListener();
        }
    }

    addRefreshListener() {
        const refreshBtn = document.getElementById('refresh-btn');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => this.handleRefresh());
        }
    }
    
    async handleRefresh() {
        try {
            const data = await this.get_stats()
    
            this.renderUI(data)
            
            // Можно добавить визуальную обратную связь
            const refreshBtn = document.getElementById('refresh-btn');
            if (refreshBtn) {
                refreshBtn.innerHTML = '<i class="bi bi-check2 me-1"></i> Обновлено';
                setTimeout(() => {
                    refreshBtn.innerHTML = '<i class="bi bi-arrow-clockwise me-1"></i> Обновить';
                }, 2000);
            }
        } catch (error) {
            console.error('Refresh failed:', error);
            const refreshBtn = document.getElementById('refresh-btn');
            if (refreshBtn) {
                refreshBtn.innerHTML = '<i class="bi bi-exclamation-triangle me-1"></i> Ошибка';
                setTimeout(() => {
                    refreshBtn.innerHTML = '<i class="bi bi-arrow-clockwise me-1"></i> Обновить';
                }, 2000);
            }
        }
    }

    renderStats(data) {
        console.log('Rendering stats:', data);
        document.getElementById('totalUsers').textContent = data.total_users;
        document.getElementById('totalPartners').textContent = data.total_partners;
        document.getElementById('monthlySales').textContent = `${data.monthly_sales.toLocaleString()} ₽`;
        document.getElementById('productTypes').textContent = data.products_types_count;
    }

    renderSalesChart(weeklySales) {
        console.log('Rendering sales chart:', weeklySales);
        const ctx = document.getElementById('salesChart');
        
        // Destroy existing chart if any
        if (Chart.getChart(ctx)) {
            Chart.getChart(ctx).destroy();
        }

        // Generate array of dates for the last week
        const today = new Date();
        const dates = Array.from({length: 7}, (_, i) => {
            const date = new Date(today);
            date.setDate(today.getDate() - (6 - i));
            return date;
        });

        // Create a map of sales data by date
        const salesMap = new Map(weeklySales.map(sale => [
            new Date(sale.date).toDateString(),
            sale.amount
        ]));

        // Prepare data for chart
        const labels = dates.map(date => date.toLocaleDateString('ru-RU', {
            day: 'numeric',
            month: 'numeric'
        }));
        
        const data = dates.map(date => salesMap.get(date.toDateString()) || 0);

        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Продажи',
                    data: data,
                    backgroundColor: '#67ba80',
                    borderRadius: 4,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return new Intl.NumberFormat('ru-RU', {
                                    style: 'currency',
                                    currency: 'RUB'
                                }).format(context.raw);
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        grid: {
                            display: false
                        }
                    },
                    y: {
                        ticks: {
                            callback: function(value) {
                                return (value / 1000) + 'k';
                            }
                        },
                        beginAtZero: true,
                    }
                }
            }
        });
    }

    

    renderRecentSales(recentSales) {
        const container = document.getElementById('recentSalesContainer');
        
        if (!recentSales || recentSales.length === 0) {
            container.innerHTML = `
                <div class="text-center p-4">
                    <div class="mb-3" style="font-size: 3rem; color: var(--green)">
                        <i class="bi bi-graph-up"></i>
                    </div>
                    <h3 class="h5 text-muted mb-2">Нет данных о продажах</h3>
                    <p class="text-muted small">Здесь будут отображаться последние заказы</p>
                    <button class="button button-primary button-lg" id="refresh-btn">
                        <i class="bi bi-arrow-clockwise me-1"></i> Обновить
                    </button>
                </div>
            `;
            this.addRefreshListener();
            return;
        }
        
        container.innerHTML = recentSales.map(sale => `
            <div class="sale-item">
                <div class="sale-info">
                    <div class="sale-company">${sale.partner_name}</div>
                    <div class="sale-product">${sale.product_name}</div>
                </div>
                <div class="sale-amount">+${sale.amount.toLocaleString()}₽</div>
            </div>
        `).join('');
    }
}

// Инициализируем дашборд при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    console.log('Initializing dashboard...');
    new Dashboard();
}); 