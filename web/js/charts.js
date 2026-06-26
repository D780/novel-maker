// 图表绘制
class ChartManager {
    constructor() {
        this.charts = {};
    }

    createPacingChart(containerId, data) {
        const ctx = document.getElementById(containerId);
        if (!ctx) return;

        // 清除现有图表
        if (this.charts[containerId]) {
            this.charts[containerId].destroy();
        }

        this.charts[containerId] = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: [{
                    label: '节奏强度',
                    data: data.values,
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 10
                    }
                }
            }
        });
    }

    createEmotionChart(containerId, data) {
        const ctx = document.getElementById(containerId);
        if (!ctx) return;

        if (this.charts[containerId]) {
            this.charts[containerId].destroy();
        }

        this.charts[containerId] = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: data.labels,
                datasets: [{
                    data: data.values,
                    backgroundColor: [
                        '#FF6384',
                        '#36A2EB',
                        '#FFCE56',
                        '#4BC0C0',
                        '#9966FF'
                    ]
                }]
            }
        });
    }
}

window.chartManager = new ChartManager();
