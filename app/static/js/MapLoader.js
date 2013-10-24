// Map Builder Javascript file for Sun Finder

// hiding functions from global scope
(function() {
	
	// Namespace - main static/global variable to reference
	var MapLoader = {}; 

	MapLoader.Map = function(mapInfo) {

	    //stops other event listeners from firing on search button
		console.log("build_map" + mapInfo.lat); // test
		
		//Pulls lat, lng from search result
		var mapLatLng = new google.maps.LatLng(mapInfo.lat, mapInfo.lng);

		var map_options = {
		  // center: new google.maps.LatLng(37.7655,-122.4429),
		  center: mapLatLng,
		  zoom: 13,
		  mapTypeId: google.maps.MapTypeId.ROADMAP
		}
		
		// Establishes Google maps
		this.map = new google.maps.Map(mapInfo.canvas, map_options);

		// Map style
		this.map.set('styles', 

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
		this.createMarker({
			position: mapLatLng, 
			imgUrl: mapInfo.searchMarkerImg,
			imgTitle: "Search Result",
			scaledSize:new google.maps.Size(27, 27)
		});

		// Add weather icon and label based on search
		if (mapInfo.weatherSearchImg){

			this.createMarker({
				position: mapLatLng, 
				imgUrl: mapInfo.weatherSearchImg,
				origin: new google.maps.Point(0,0),
				// size: new google.maps.Size(20, 32),
				anchor: new google.maps.Point(0,0),
				scaledSize:new google.maps.Size(27, 27)
			});
		
	    	this.createLabel({ 
	    		lat: mapInfo.lat,
	    		lng: mapInfo.lng,
	    		labelContent: mapInfo.weatherSearchLabel
	    	});
		}
		
	};
	
	// Applying to Map prototype for function reference on the instance of map
	MapLoader.Map.prototype.renderMarkers = function(data){
		
		if (data){
			var locations = data.locations;

			for (var i = 0; i < locations.length; i++) {
		    	this.createMarker({
		    		imgUrl:locations[i].img_url,
		    		position: new google.maps.LatLng(locations[i].lat, locations[i].lng), 
					origin: locations.origin || new google.maps.Point(0,0),
					anchor: locations.anchor || new google.maps.Point(0,0),
					scaledSize: new google.maps.Size(25, 25)
		    	});

		    	this.createLabel({ 
		    		lat: locations[i].lat,
		    		lng: locations[i].lng,
		    		labelContent: locations[i].temp_range, 
		    	});

		  	}     
		};

	};

	// Add images to map
	MapLoader.Map.prototype.createMarker = function(data) {
		var markerImg = {
			scaledSize: new google.maps.Size(20, 25),
			size: new google.maps.Size(25, 32),
			url: data.imgUrl,
			origin: data.origin,
			anchor: data.anchor,
			scaledSize: data.scaledSize,
		};

		var makeMarker = new google.maps.Marker({
			map: this.map,
		    position: data.position,
		    draggable: false,
	    	raiseOnDrag: false,
			icon: markerImg,
			title: data.imgTitle
		});

	}

	// MarkerWith Label - add labels on map
	MapLoader.Map.prototype.createLabel = function(data) {
		new MarkerWithLabel({
	       position: new google.maps.LatLng(data.lat,data.lng),
	       draggable: false,
	       raiseOnDrag: false,
	       map: this.map,
	       labelInBackground: false, //Keeps label in the front
	       labelContent: data.labelContent,
	       labelAnchor: new google.maps.Point(35, 10),
	       labelClass: "labels", // Connects to CSS class label
		});
	}

	// make global var accessible externally
	window.MapLoader = MapLoader; 

	
})();