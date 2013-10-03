// Main Javascript file for Sun Finder

// hiding functions from global scope
(function() {
	
	// Namespace - main static/global variable to reference
	var MapLoader = {}; 

	console.log("main js"); // Confirm load

	// Load map  - currently SF biased
	function buildMap(canvas, lat, lng, searchMarkerImg, weatherSearchImg) { 

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

		// Create search results marker
		createMarker({
			position: mapLatLng, 
			map: map, 
			imgUrl: searchMarkerImg,
			imgTitle: "Search Result",
			scaledSize:new google.maps.Size(27, 27)
		});

		if (weatherSearchImg){
			console.log(weatherSearchImg);

			createMarker({
				position: mapLatLng, 
				map: map, 
				imgUrl: weatherSearchImg,
				origin: new google.maps.Point(0,0),
				// size: new google.maps.Size(20, 32),
				anchor: new google.maps.Point(0,0),
				scaledSize:new google.maps.Size(27, 27)
			});
		}
		
		callMarkerData(map);

	}
	
	// Add images to map
	function createMarker(data) {
		var markerImg = {
			scaledSize: new google.maps.Size(20, 25),
			size: new google.maps.Size(25, 32),
			url: data.imgUrl,
			origin: data.origin,
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

	// MarkerWith Label - add labels on map
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

	function renderMarkers(map, locations) { 
		for (var i = 0; i < locations.length; i++) {
	    	createMarker({
	    		imgUrl:locations[i].img_url,
				map: map, 
	    		position: new google.maps.LatLng(locations[i].lat, locations[i].lng), 
				origin: locations.origin || new google.maps.Point(0,0),
				anchor: locations.anchor || new google.maps.Point(0,0),
				scaledSize: new google.maps.Size(25, 25)
	    	});

	    	createLabel({ 
	    		lat: locations[i].lat,
	    		lng: locations[i].lng,
	    		labelContent: locations[i].temp_range, 
	    		map: map
	    	});

	  	}     
	 }

	function callMarkerData(map) {
		$.ajax({
			url:'map_details',
			type: "GET",
			cache: false,
			dataType: "json",
			success: function(data){
				renderMarkers(map, data.locations);
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

		// Create search marker
		var searchMarkerImg = "https://maps.gstatic.com/mapfiles/icon_green.png";

		// $('#sun_finder_title').show();
		$('#page_results').show();
				 
		if (options.lat){
			buildMap(options.mapCanvas,options.lat,options.lng, searchMarkerImg, options.pic);

		} else if (navigator.geolocation) {
		    navigator.geolocation.getCurrentPosition(function(position) {

		        var geo_lat = position.coords.latitude;
		        var geo_lng = position.coords.longitude;
				
				$('#coord').val(lat + ',' + lng);
		        console.log($('#index_coord').val());
		        buildMap(options.mapCanvas, geo_lat, geo_lng, searchMarkerImg);

		    }, function(error) {
			    console.log('geolocation not exist');
			    lat = 
		        buildMap(options.mapCanvas, lat, lng, searchMarkerImg);
			});
		} else {
		    // Fallback for no geolocation
		    console.log('geolocation not shared');
		    buildMap(options.mapCanvas, lat, lng, searchMarkerImg);
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