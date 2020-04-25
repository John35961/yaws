// Instanciating new map

let weatherCurrentMap = new L.map('weather_current_map', {
                                  fullscreenControl: {
                                      pseudoFullscreen: true
                                  }})
                            .setView([48.8534, 2.3488], 7);


// Adapting map tiles to selected CSS theme,
// when DOM is ready, or checkbox is clicked

adaptMapTheme = function() {
    if ($('#darkSwitch').is(':checked')) {
        L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 17,
        minZoom: 3
        }).addTo(weatherCurrentMap);
    }
    else {
        L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager_labels_under/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 17,
        minZoom: 3
        }).addTo(weatherCurrentMap);
    }
};

$(document).ready(function() {
    adaptMapTheme();
});

$('#darkSwitch').click(function() {
    adaptMapTheme();
});


// Adding a click event to the map,
// so that the user can access weather data by clicking
// a given location

let lat, lon;

weatherCurrentMap.addEventListener('click', function(ev) {
    
    clickedCoordinates = {
        lat: ev.latlng.lat,
        lon: ev.latlng.lng
    };

    let request = new XMLHttpRequest();

    opwmCelJson = `/map_click?lat=${clickedCoordinates['lat']}&lon=${clickedCoordinates['lon']}`;
    
    request.open('GET', opwmCelJson);
    
    request.onload = function() {
        let data = JSON.parse(this.response);
        
        try {
            var locationStationName = data.name;
            var countryCode = `(${data.sys.country})`;
            var weatherCelTempCurrent = `<h5>${data.main.temp.toFixed(1)}</h5>
                                         <h6>°C</h6>`;
            var moreBtn = `<a href="/?location=${locationStationName}" target="_blank">
                                <button class="btn btn-outline-primary mb-2">More<i class="fas fa-chevron-right pl-2"></i></button>
                           </a>`;

            if (data.main.temp_min.toFixed(1) != data.main.temp_max.toFixed(1)) {
                weatherCelTempRange = `<h5>${data.main.temp_min.toFixed(1)}</h5>
                                       <h6 class="pr-2">°C</h6>
                                       <h5 class="pr-2">to</h5>
                                       <h5>${data.main.temp_max.toFixed(1)}</h5>
                                       <h6 class="pr-2">°C</h6>`;
            } else {
                var weatherCelTempRange = `<h5>No data</h5>`;
            };

            if (data.name == '') {
                locationStationName = 'Imprecise location';
                countryCode = '';
                moreBtn = '';
            };

        } catch (e) {
            console.log(e); 
            locationStationName = 'Imprecise location';
            countryCode = '';
            weatherCelTempCurrent = `<h5>No data</h5>`;
            weatherCelTempRange = `<h5>No data</h5>`;
            moreBtn = '';
        };

        L.popup()
        .setLatLng([clickedCoordinates['lat'], 
                    clickedCoordinates['lon']])
        .setContent(`<h4>${locationStationName} ${countryCode}</h4>
                    <hr/>
                    <div class="row mt-3 mr-3">
                        <div class="col-md-12">
                            <div class="pb-3">
                                <div class="d-flex">
                                    ${weatherCelTempCurrent}
                                </div>
                                <p class="secondary no-select pb-4">Current temperature</p>
                                <div class="d-flex">
                                    ${weatherCelTempRange}
                                </div>
                                <p class="secondary no-select pb-4">Temperature range</p>
                            </div>
                        </div>
                    </div>
                    ${moreBtn}`)
        .openOn(weatherCurrentMap);
        $('.leaflet-popup-close-button').addClass('no-select');
    };
    
    request.send();

});