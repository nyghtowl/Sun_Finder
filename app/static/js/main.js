// Main Javascript file for Sun Finder

// hiding functions from global scope
(function() {
	
	// Namespace - main static/global variable to reference
	var MapLoader = {}; 

	console.log("main js"); // Confirm load

	// Load map  - currently SF biased
	function buildMap(canvas, lat, lng) { 

	    //stops other event listeners from firing on search button
		console.log("build_map" + lat); // test
		
		//Pulls lat, lng from search result
		var mapLatLng = new google.maps.LatLng(lat, lng);

		var map_options = {
		  // center: new google.maps.LatLng(37.7655,-122.4429),
		  center: mapLatLng,
		  zoom: 13,
		  mapTypeId: google.maps.MapTypeId.ROADMAP
		}
		
		// Establishes Google maps
		var map = new google.maps.Map(canvas, map_options);

		// Map style
		map.set('styles', 

			[
			  {
			    "featureType": "administrative.country",
			    "stylers": [
			      { "visibility": "off" }
			    ]
			  },{
			    "featureType": "administrative.province",
			    "stylers": [
			      { "visibility": "off" }
			    ]
			  },{
			    "featureType": "administrative.neighborhood",
			    "elementType": "labels.text.fill",
			    "stylers": [
			      { "visibility": "on" },
			      { "saturation": -100 },
			      { "lightness": -12 }
			    ]
			  },{
			    "featureType": "landscape.man_made",
			    "elementType": "labels.text.stroke",
			    "stylers": [
			      { "visibility": "off" }
			    ]
			  },{
			  },{
			    "featureType": "transit.station",
			    "stylers": [
			      { "visibility": "simplified" }
			    ]
			  },{
			    "featureType": "road",
			    "stylers": [
			      { "visibility": "simplified" }
			    ]
			  },{
			    "featureType": "poi",
			    "stylers": [
			      { "visibility": "simplified" }
			    ]
			  },{
			    "featureType": "poi.park",
			    "elementType": "labels.text.fill",
			    "stylers": [
			      { "visibility": "on" }
			    ]
			  },{
			    "featureType": "road.arterial",
			    "stylers": [
			      { "visibility": "off" }
			    ]
			  },{
			  }
			]
			);

		// Generating the weather image
		var weatherImg = {
			url:'static/img/partly_cloudy_small.png',
			origin: new google.maps.Point(0,0),
			// size: new google.maps.Size(20, 32),
			anchor: new google.maps.Point(20,32)
		};

        var weatherMarker = new google.maps.Marker({
			position: mapLatLng,
			map: map,
			icon: weatherImg,
			title: "Something"
		});
        
		singleMapMarker(mapLatLng, map);
		// mutipleMapMarks(map);
	}

// pass coordinates and so forth to marker creator
	// Search result single green marker
	function singleMapMarker(position, map) {
		var markerImg = {
			scaledSize: new google.maps.Size(20, 25),
			size: new google.maps.Size(25, 32),
			url: "https://maps.gstatic.com/mapfiles/icon_green.png"
		};

		var marker = new google.maps.Marker({
		    position: position,
		    draggable: false,
	    	raiseOnDrag: false,
			map: map,
			icon: markerImg,
			title: "Search Result"
		});

	}

	// MarkerWith Label - add multiple markers on the map
	function createMarker(position, label, map) {
		return new MarkerWithLabel({
	       position: new google.maps.LatLng(position[0],position[1]),
	       draggable: false,
	       raiseOnDrag: false,
	       map: map,
	       labelContent: label,
	       labelAnchor: new google.maps.Point(22, 0),
	       labelClass: "labels", // Connects to CSS class label
	       labelStyle: {opacity: 1}
		});
	}

// function addWeatherInfo(position, icon, temp, map){
	// return new google.maps.Marker({
	// 		position: position[0], position[1]
	// 		map: map,
	// 		icon: icon
	// 	});
// }

	function readData(positions, labels, map) { 
		for (var i = 0; i < positions.length; i++) {
	    	createMarker(positions[i], labels[i], map);
	    	//addWeatherInfo(positions[i], icons[i], temps[i], map) Have function to add icon and temp
	  	}     
	 }

	function mutipleMapMarks(map) {
		$.ajax({
			url:'map_details',
			type: "GET",
			cache: false,
			dataType: "json",
			success: function(data){
				readData(data.result.loc_coords, data.result.locations,map);
				// take data of current weather icon and temp from cache for list of locations
				}
		});
	}

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
	// Other pages map load
	MapLoader.pageSetup = function(options)	{
		// Pre-set lat lng to SF if not provided
		var lat = 37.7655;
		var lng = -122.4429;

		// $('#sun_finder_title').show();
		$('#page_results').show();
				 
		if (options.lat){
			buildMap(options.mapCanvas,options.lat,options.lng);

		} else if (navigator.geolocation) {
		    navigator.geolocation.getCurrentPosition(function(position) {

		        var geo_lat = position.coords.latitude;
		        var geo_lng = position.coords.longitude;
				
				$('#coord').val(lat + ',' + lng);
		        console.log($('#index_coord').val());
		        buildMap(options.mapCanvas, geo_lat, geo_lng);

		    }, function(error) {
			    console.log('geolocation not exist');
			    lat = 
		        buildMap(options.mapCanvas, lat, lng);
			});
		} else {
		    // Fallback for no geolocation
		    console.log('geolocation not shared');
		    buildMap(options.mapCanvas, lat, lng);
		}

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
	window.MapLoader = MapLoader; 

	
})();