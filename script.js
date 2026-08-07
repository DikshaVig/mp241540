document.addEventListener('DOMContentLoaded', function () {
    const ctx = document.getElementById('metricsChart');
    
    if (ctx) {
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['K-Means', 'Agglomerative', 'Hierarchical', 'DBSCAN'],
                datasets: [{
                    label: 'Silhouette Score',
                    data: [0.554, 0.523, 0.518, 0.412],
                    backgroundColor: [
                        '#1d5bd8',
                        '#94a3b8',
                        '#94a3b8',
                        '#94a3b8'
                    ],
                    borderRadius: 8,
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 0.7,
                        grid: {
                            color: '#e2e8f0'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }
});