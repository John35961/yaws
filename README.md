# [yaws.me](http://yaws.me)
Simple weather application made with Python, Flask and AWS Elastic Beanstalk.

## Change Log
__1.5.1__
- In map mode, enhanced handling of remote areas clicks, on which often very little data is available, via try/catch use

__1.5.0__
- Added a dark mode, relying on dark-mode-switch, to be toggled via a switch
- Reorganized JS files and imports
- Added CSS theme variables for better scalability

__1.4.0__
- Added a map mode relying on Leaflet
- Added /map_click route, dedicated to map mode, to make calls to OpenWeatherMap API in the backend
- On /map_click route, added a limiter decorator (Flask-Limiter) to prevent user from hitting the OpenWeatherMap API calls rate limit (60/minute)

__1.3.1__
- Fixed header search-bar's CSS to prevent button from falling under when resizing
- Moved JS code in separate files
- Isolated footer in footer.html
- Removed unnecessary footer on HTTP error pages
- Fixed typos

__1.3.0__
- Added  Celsius / Fahrenheit radio button for user to chose the unit of current temperature, temperature range and current wind speed 
- Added Celsius / Fahrenheit support to the 5 days forecast chart accordingly
- Unified variables naming 

__1.2.2__
- PEP 8 refactoring
- Deleted unused variable "request_server_datetime" in application.py
- Did various typeahead.js CSS and Bootstrap classes adjustments

__1.2.1__
- Added JS conditional highlighting for UV index and air quality index
- Added support for US, Spanish, Italian, German and UK cities in typeahead.js
- Corrected various typos in about.html
- Mentioned the use of typeahead.js in about.html
- Removed useless import of csv module
- Enriched .gitignore

__1.2.0__
- Added UV index from OpenWeatherMap API 
- Added air quality index from AirVisual API

__1.1.0__
- Implemented typeahead.js for user's input

__1.0.0__
- Initial release
