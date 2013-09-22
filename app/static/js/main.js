// Main Javascript file for Sun Finder

(function() {
	// Confirm load
	console.log("main js");


	// Load map  - currently SF biased
	function buildMap(container, map_lat, map_long) { 

		// Pre-set lat lng to SF if not provided
		if (!map_lat || !map_long) {
			map_lat = 37.7655;
			map_long = -122.4429;
		}
	    //stops other event listeners from firing on search button
		console.log("build_map" + map_lat); // test
		
		//Pulls lat, lng from search result
		var myLatLng = new google.maps.LatLng(map_lat,map_long);

		var map_options = {
		  // center: new google.maps.LatLng(37.7655,-122.4429),
		  center: myLatLng,
		  zoom: 13,
		  mapTypeId: google.maps.MapTypeId.ROADMAP
		}
		
		// Establishes Google maps
		var map = new google.maps.Map(container, map_options)

		// Map style
		// map.set('styles', [
		//   {
		//     featureType: 'all',
		//     elementType: 'all',
		//     stylers: [
		//       { weight: 0.6 },
		//       { lightness: -12 }
		//     ]
		//   },
		//   {
		//     featureType: 'all',
		//     elementType: 'labels',
		//     stylers: [
		//       { visibility: 'off' }
		//     ]
		//   }
		// ]);

		// Generating the weather image
		var weatherImg = {
			url:'static/img/partly_cloudy_small.png',
			origin: new google.maps.Point(0,0),
			// size: new google.maps.Size(20, 32),
			anchor: new google.maps.Point(20,32)
		};

  //       var weatherMarker = new google.maps.Marker({
		// 	position: myLatLng,
		// 	map: map,
		// 	// icon: weatherImg,
		// 	title: "Something"
		// });
        
		// Search result single green marker
		var markerImg = {
			scaledSize: new google.maps.Size(20, 25),
			size: new google.maps.Size(25, 32),
			url: "https://maps.gstatic.com/mapfiles/icon_green.png"
		};

		var marker = new google.maps.Marker({
		    position: myLatLng,
		    draggable: false,
	    	raiseOnDrag: false,
			map: map,
			icon: markerImg,
			title: "Search Result"
		});


		// mutipleMapMarks(map);
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


	// Build map index initializer
	function indexLoadMap(canvas_search){
		console.log('index load map');

		lat = 37.7888;
		lng = -122.4037;
		if (navigator.geolocation) {

		    navigator.geolocation.getCurrentPosition(function(position) {

		        lat = position.coords.latitude;
		        lng = position.coords.longitude;

				$('#index_coord').val(lat + ',' + lng);
				console.log($('#index_coord').val());

		        buildMap(canvas_search, lat, lng);

		    }, function(error) {
			    console.log('geo loc not exist');
		        buildMap(canvas_search, lat, lng);
			});

		} else {
		    // Fallback for no geolocation
		    console.log('geoloc not shared');
		    buildMap(canvas_search, lat, lng);
		}
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


	// Load search bar
	$(function(){
		
		var canvas_search = document.getElementById('map_canvas_search');

		$('.sun_submit').on('click', function() { 
			$('#layout_body_container').hide();
			$("#spinner").show() 
		});

		if (document.getElementById('index_form_load')){
			console.log('index load');
			
			$('#layout_body_container').show();

			typeahead();
			datepicker();
			indexLoadMap(canvas_search);

		}else{
			console.log('not index');
			$('#sun_finder_title').show();
			
			if (typeof resultsLoad !== 'undefined') {
				resultsLoad();
			}
			
			$.ajax({
				type: "GET",
				url: "form_top_partial",
				success: function(data) { 
					$('#layout_body_container').show();
					$('#top_form_load').append(data); 
					var canvas_search = document.getElementById('map_canvas_search');
					var canvas_results = document.getElementById('map_canvas_results');

					if (lastSearchLocation) {
						buildMap(canvas_search, lastSearchLocation.lat, lastSearchLocation.lng);
						buildMap(canvas_results, lastSearchLocation.lat, lastSearchLocation.lng);
					}		
					typeahead();
					datepicker();

				},
				dataType: 'html'
			});

		}	

	});

})();