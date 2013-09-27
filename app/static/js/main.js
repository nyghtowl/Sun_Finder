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


		// Create search marker
		var searchMarkerImg = "https://maps.gstatic.com/mapfiles/icon_green.png";
		
		createMarker({
			position: mapLatLng, 
			map: map, 
			imgUrl: searchMarkerImg,
			imgTitle: "Search Result",
			scaledSize:new google.maps.Size(27, 27)
		});

		// Generating the weather image        
        var weatherMarkerImg = 'static/img/partly_cloudy_small.png';
		
		createMarker({
			position: mapLatLng, 
			map: map, 
			imgUrl: weatherMarkerImg,
			origin: new google.maps.Point(0,0),
			// size: new google.maps.Size(20, 32),
			anchor: new google.maps.Point(0,0),
			scaledSize:new google.maps.Size(27, 27)
		});

		var locations = [

		[37.7698, -122.4472, 13, 'Haight Ashbury', weatherMarkerImg, "56.7 F"],

		[37.7514, -122.4316, 13, 'Noe Valley', weatherMarkerImg, "56.7 °F"],
		[37.7516, -122.4477, 13, 'Twin Peaks', weatherMarkerImg, "56.7 °F"],
		[37.7627, -122.4352, 13, 'Castro', weatherMarkerImg, "56.7 °F"],
		[37.7727, -122.4283, 13, 'Hayes Valley', weatherMarkerImg, "56.7 °F"],
		[37.7600, -122.4148, 13, 'Mission District', weatherMarkerImg, "56.7 °F"],
		[37.7572, -122.3999, 13, 'Potrero', weatherMarkerImg, "56.7 °F"]

		];

		readData(map, locations);

	}

	// Search result single green marker
	function createMarker(data) {
		var markerImg = {
			scaledSize: new google.maps.Size(20, 25),
			size: new google.maps.Size(25, 32),
			url: data.imgUrl,
			origin: data.origin || new google.maps.Point(0,0),
			anchor: data.anchor,
			scaledSize: data.scaledSize,
		};

		var makeMarker = new google.maps.Marker({
		    position: data.position,
		    draggable: false,
	    	raiseOnDrag: false,
			map: data.map,
			icon: markerImg,
			title: data.imgTitle
		});

	}

	// MarkerWith Label - add multiple markers on the map
	function createLabel(data) {
		return new MarkerWithLabel({
	       position: new google.maps.LatLng(data.lat,data.lng),
	       draggable: false,
	       raiseOnDrag: false,
	       map: data.map,
	       labelInBackground: false, //Keeps label in the front
	       labelContent: data.labelContent,
	       labelAnchor: new google.maps.Point(35, 10),
	       labelClass: "labels", // Connects to CSS class label
		});
	}


	function readData(map, locations) { 
		for (var i = 0; i < locations.length; i++) {
	    	console.log(locations[i][5]);
	    	createLabel({ 
	    		lat: locations[i][0],
	    		lng: locations[i][1],
	    		labelContent: locations[i][5], 
	    		map: map
	    	});
	    	createMarker({
	    		imgUrl:locations[i][4],
	    		position: new google.maps.LatLng(locations[i][0], locations[i][1]), 
				map: map, 
				scaledSize:new google.maps.Size(25, 25)
	    	});
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