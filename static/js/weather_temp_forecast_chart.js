let ctx = document.getElementById('weather_temp_forecast_chart').getContext('2d');
let  weather_temp_forecast_chart = new Chart(ctx, 
{
    type: 'line',
    data: {
        labels: chartLabels,
        datasets: [{
            label: 'Temperature (°C)',
            data: chartCelData,
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

adaptChartTheme = function() {
    if ($('#darkSwitch').is(':checked')) {
        weather_temp_forecast_chart.data.datasets[0].backgroundColor = 'rgba(222, 113, 25, 0.3)';
        weather_temp_forecast_chart.data.datasets[0].borderColor = 'rgba(222, 113, 25, 1)';
        weather_temp_forecast_chart.update();
    } else {
        weather_temp_forecast_chart.data.datasets[0].backgroundColor = 'rgba(0, 123, 255, 0.3)';
        weather_temp_forecast_chart.data.datasets[0].borderColor = 'rgba(0, 123, 255, 1)';
        weather_temp_forecast_chart.update();
    };
}

$(document).ready(function(){
    adaptChartTheme();
});


$('#darkSwitch').click(function() {
    adaptChartTheme();
});