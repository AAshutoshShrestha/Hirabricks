// temperature-chart using a library like Chart.js
var ctx = document.getElementById('temperature-chart').getContext('2d');
var temperatureChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        datasets: [{
            label: 'Average Temperature',
            data: [10, 12, 11, 14, 15, 13], // Replace with actual data
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    }
});


// car-status-chart using a library like Chart.js
var ctx = document.getElementById('car-status-chart').getContext('2d');
var carStatusChart = new Chart(ctx, {
    type: 'pie',
    data: {
        labels: ['Inline', 'Completed'],
        datasets: [{
            label: 'Car Status',
            data: [80, 20], // Replace with actual data
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    }
});
