// Main Javascript file for Sun Finder

// hiding functions from global scope
(function() {
	
	// Namespace - main static/global variable to reference
	var PageLoader = {}; 

	var SEARCH_IMG_URL = 'https://maps.gstatic.com/mapfiles/icon_green.png';

	// console.log("main js"); // Confirm load


	// Typeahead - Autocomplete
	function typeahead() {
		console.log("typeahead"); //test

		$("#sun_query").typeahead({
		    minLength: 1,
		    source: function (query, process) {
		        return $.post(
		            '/autocomplete', 
		            { msg: query }, 
		            function (data) {
		            	var data = JSON.parse(data)
		                return process(data.options);
		        });
		    }
		});
	}


	// Datepicker
	function datepicker() {
		console.log("datepicker"); //test
		$( ".datepicker" ).datepicker({dateFormat: "mm-dd-yy",
			minDate: "0d",
			maxDate: "+3d"
		});
	}

	function getCoordinates(options) {
		options = options || { };
		return new RSVP.Promise(function (resolve, reject) {

			// Pre-set lat lng to SF if not provided
			var defaults = { lat: 37.7655, lng: -122.4429 };

			if (options.lat) {
				resolve({ lat: options.lat, lng: options.lng });
				console.log ('inside get Coord and options', options.lat, options.lng)
			} else if (navigator.geolocation) {
			    navigator.geolocation.getCurrentPosition(function(position) {
					resolve({
						lat: position.coords.latitude,
						lng: position.coords.longitude,
						source: 'geolocation'
					});
				}, function () {
					resolve(defaults);
				});
			} else {
				resolve(defaults);
			}

		});
	}

	// Provides clean error output
	RSVP.configure('onerror', function(e) {
	  console.error(e.message); 
	  console.error(e.stack);
	});

	// Other pages map load
	PageLoader.pageSetup = function(options)	{
		// default if nothing passed
		options = options || {};

		// $('#sun_finder_title').show();
		$('#page_results').show();

		getCoordinates(options).then(function (coords) {

			if (coords.source === 'geolocation') {
			    // Stores coord in form to help specify api search location
				$('#coord').val(coords.lat + ',' + coords.lng);
			}


			// Ajax request handled separately and this can be built immediately, thus pulled out buildMaps
			var searchMap = new MapLoader.Map({
				canvas:$('#map_canvas_search')[0],	
				lat: coords.lat,
				lng: coords.lng, 
				searchMarkerImg: SEARCH_IMG_URL, 
				weatherSearchImg: options.pic,
				weatherSearchLabel: options.searchLabel,
			});

			if ($('#map_canvas_results').length){

				var resultsMap = new MapLoader.Map({
					canvas:$('#map_canvas_results')[0],	
					lat: coords.lat,
					lng: coords.lng, 
					searchMarkerImg: SEARCH_IMG_URL, 
					weatherSearchImg: options.pic,
					weatherSearchLabel: options.searchLabel
				});			
			}

			// Ajax pulls Redis stored daily weather data - applies to map after developed
			$.ajax({
				url:'map_details',
				type: "GET",
				cache: false,
				dataType: "json"
			}).then(function (multipleWeatherData) {
				searchMap.renderMarkers(multipleWeatherData);
				if (resultsMap){
					resultsMap.renderMarkers(multipleWeatherData);
				}
			});

		});

		typeahead();
		datepicker();
	}

	// Setup search event 
	$(function(){
		
		$('.sun_submit').on('click', function() { 
			$('.page_results').hide();
			$('#spinner').show();
		});
	});

	// make global var accessible externally
	window.PageLoader = PageLoader; 

	
})();