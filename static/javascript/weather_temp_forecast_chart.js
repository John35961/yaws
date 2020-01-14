let ctx = document.getElementById('weather_temp_forecast_chart').getContext('2d');
let  weather_temp_forecast_chart = new Chart(ctx, 
{
    type: 'line',
    data: {
        labels: chartLabels,
        datasets: [{
            label: 'Temperature (°C)',
            data: chartCelData,
            backgroundColor: [
                'rgba(0, 123, 255, 0.3)'
            ],
            borderColor: [
                'rgba(0, 123, 255, 1)'
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