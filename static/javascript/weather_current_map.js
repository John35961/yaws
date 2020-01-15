let weatherCurrentMap = L.map('weather_current_map').setView([48.8534, 2.3488], 7);

L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager_labels_under/{z}/{x}/{y}{r}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 19
}).addTo(weatherCurrentMap);

let lat, lng;

weatherCurrentMap.addEventListener('click', function(ev) {
    clicked_coordinates = {
        lat: ev.latlng.lat,
        lng: ev.latlng.lng
    };
    let request = new XMLHttpRequest();
    opwm_cel_json = `https://api.openweathermap.org/data/2.5/weather?lat=${clicked_coordinates['lat']}&lon=${clicked_coordinates['lng']}&appid=6d6a8a1723819a00e3a2aa6310cfccce&units=metric`
    request.open('GET', opwm_cel_json);
    request.onload = function() {
        let data = JSON.parse(this.response);
        try {
            location_station_name = data.name;
            if (data.name == '') {
                location_station_name = 'Imprecise location';
            }
            country_code = `(${data.sys.country})`;
            if (typeof data.sys.country == 'undefined') {
                country_code = '';    
            }
            weather_cel_temp_current = data.main.temp.toString();
            weather_cel_temp_min = data.main.temp_min.toString();
            weather_cel_temp_max = data.main.temp_max.toString();

        } catch (e) {
            console.log(e); 
            weather_cel_temp_current = 'No temperature found!';
        };
        L.popup()
        .setLatLng([clicked_coordinates['lat'], 
                    clicked_coordinates['lng']])
        .setContent(`<h4>${location_station_name} ${country_code}</h4>
                    <hr/>
                    <div class="row mt-3 mr-3">
                        <div class="col-md-12">
                            <div class="pb-3">
                                <div class="d-flex">
                                    <h5>${weather_cel_temp_current}</h5>
                                    <h6>°C</h6>
                                </div>
                                <p class="secondary pb-4">Current temperature</p>
                                <div class="d-flex">
                                    <h5>${weather_cel_temp_min}</h5>
                                    <h6 class="pr-2">°C</h6>
                                    <h5 class="pr-2">to</h5>
                                    <h5>${weather_cel_temp_max}</h5>
                                    <h6 class="pr-2">°C</h6>
                                </div>
                                <p class="secondary pb-4">Temperature range</p>
                            </div>
                        </div>
                    </div>
                    <a href="http://localhost:5000/?location=${location_station_name}" target="_blank">
                        <button class="btn btn-outline-primary mb-2">More<i class="fas fa-chevron-right pl-2"></i></button>
                    </a>`)
        .openOn(weatherCurrentMap);
    };
    request.send();
});