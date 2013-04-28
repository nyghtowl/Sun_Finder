// Main Javascript file for Sun Finder

//load the visualization API with the map package
// google.load("visualization", "1", {packages: ["map"]});

// load map of SF
function initialize() {
	var map_canvas = document.getElementById('map_canvas');
	var map_options = {
	  // center: new google.maps.LatLng(37.7655,-122.4429),
	  center: new google.maps.LatLng(map_lat,map_long),

	  zoom: 13,
	  mapTypeId: google.maps.MapTypeId.ROADMAP
	}
	map = new google.maps.Map(map_canvas, map_options)
	map.set('styles', [
	  {
	    featureType: 'all',
	    elementType: 'all',
	    stylers: [
	      { weight: 0.6 },
	      { lightness: -12 }
	    ]
	  },
	  {
	    featureType: 'all',
	    elementType: 'labels',
	    stylers: [
	      { visibility: 'off' }
	    ]
	  }
	]);
	// google automatic map layer from weather.com - doesn't provide as much detail for neighborhood but good example
	var weatherLayer = new google.maps.weather.WeatherLayer({
    	temperatureUnits: google.maps.weather.TemperatureUnit.FAHRENHEIT
  	});
  	//weatherLayer.setMap(map);
}

google.maps.event.addDomListener(window, 'load', initialize);
