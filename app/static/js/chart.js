document.addEventListener('DOMContentLoaded', function() {
    var ctxAge = document.getElementById('ageChart').getContext('2d');
    var ageData = [10, 20, 30, 40, 50];  // Sample data for age chart

    var ageChart = new Chart(ctxAge, {
        type: 'bar',
        data: {
            labels: ['0-20', '21-40', '41-60', '61+'],
            datasets: [{
                label: 'Number of Patients',
                data: ageData,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)'
                ],
                borderColor: [
                    'rgba(255,99,132,1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    stepSize: 1
                }
            }
        }
    });

    var ctxImage = document.getElementById('imageChart').getContext('2d');
    var imageData = [30, 70];  // Sample data for image classification chart

    var imageChart = new Chart(ctxImage, {
        type: 'bar',
        data: {
            labels: ['Tumorous', 'Non-Tumorous'],
            datasets: [{
                label: 'Number of Images',
                data: imageData,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                ],
                borderColor: [
                    'rgba(255,99,132,1)',
                    'rgba(54, 162, 235, 1)',
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    stepSize: 10
                }
            }
        }
    });
});
