document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('salesChart');
    
    if (ctx) {
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['1 Июн', '5 Июн', '10 Июн', '15 Июн', '20 Июн', '25 Июн', '30 Июн'],
                datasets: [{
                    label: 'Продажи',
                    data: [120000, 240000, 180000, 350000, 290000, 410000, 380000],
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
                        }
                    }
                }
            }
        });
    }
}); 