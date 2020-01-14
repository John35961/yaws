if (weatherUvIndex <= 2) {
    $('#weather_uv_index').css('color', '#27ae60');
}
else if (weatherUvIndex >= 3 && weatherUvIndex <= 5) {
    $('#weather_uv_index').css('color', '#f1c40f');
}
else if (weatherUvIndex >= 6 && weatherUvIndex <= 7) {
    $('#weather_uv_index').css('color', '#e67e22');
}
else if (weatherUvIndex >= 8 && weatherUvIndex <= 10) {
    $('#weather_uv_index').css('color', '#e74c3c');
}
else {
    $('#weather_uv_index').css('color', '#9b59b6');
};

if (weatherAirQualityIndex <= 50) {
    $('#weather_air_quality_index').css('color', '#27ae60');
}
else if (weatherAirQualityIndex >= 51 && weatherAirQualityIndex <= 100) {
    $('#weather_air_quality_index').css('color', '#f1c40f');
}
else if (weatherAirQualityIndex  >= 101 && weatherAirQualityIndex <= 150) {
    $('#weather_air_quality_index').css('color', '#e67e22');
}
else if (weatherAirQualityIndex  >= 151 && weatherAirQualityIndex <= 200) {
    $('#weather_air_quality_index').css('color', '#e74c3c');
}
else if (weatherAirQualityIndex  >= 201 && weatherAirQualityIndex <= 300) {
    $('#weather_air_quality_index').css('color', '#9b59b6');
}
else {
    $('#weather_air_quality_index').css('color', '#654321');
};

function toCelsius() {
    $('.weather_temp_current').html(weatherCelTempCurrent);
    $('.weather_temp_min').html(weatherCelTempMin);
    $('.weather_temp_max').html(weatherCelTempMax);
    $('.weather_wind_speed').html(weatherCelWindSpeed);
    $('.weather_temp_unit').html('°C');
    $('.weather_wind_speed_unit').html('m/s');
    weather_temp_forecast_chart.data.datasets[0].data = chartCelData;
    weather_temp_forecast_chart.data.datasets[0].label = 'Temperature (°C)';
    weather_temp_forecast_chart.update();
};

function toFahrenheit() {
    $('.weather_temp_current').html(weatherFarTempCurrent);
    $('.weather_temp_min').html(weatherFarTempMin);
    $('.weather_temp_max').html(weatherFarTempMax);
    $('.weather_wind_speed').html(weatherFarWindSpeed);
    $('.weather_temp_unit').html('°F');
    $('.weather_wind_speed_unit').html('mi/h');
    weather_temp_forecast_chart.data.datasets[0].data = chartFarData;
    weather_temp_forecast_chart.data.datasets[0].label = 'Temperature (°F)';
    weather_temp_forecast_chart.update();
};