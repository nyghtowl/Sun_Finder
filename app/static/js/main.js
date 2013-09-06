// Main Javascript file for Sun Finder

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

	singleMapMark(map, myLatLng);
    mutipleMapMarks(map);

}


function singleMapMark(map, myLatLng){
	// Search result marker - custom img and marker variable
	var img_map = {
		scaledSize: new google.maps.Size(20, 25),
		size: new google.maps.Size(25, 32),
		url: "https://maps.gstatic.com/mapfiles/icon_green.png",
	};

	var marker = new google.maps.Marker({
	    position: myLatLng,
	    draggable: false,
    	raiseOnDrag: false,
		map: map,
		icon: img_map,
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


function readData(positions, labels, map) { 
	for (var i = 0; i < positions.length; i++) {
    	createMarker(positions[i], labels[i], map);
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
			}
	});
}


// Build map index initializer
function indexLoadMap(){
	console.log('index load map');

	lat = 37.7888;
	lng = -122.4037;
	if (navigator.geolocation) {

	    navigator.geolocation.getCurrentPosition(function(position) {

	        lat = position.coords.latitude;
	        lng = position.coords.longitude;

	        console.log(lat + ' ' + lng);
	        buildMap($('#map_canvas_search')[0], lat, lng);

	    }, function(error) {
		    console.log('geo loc not exist');
	        buildMap($('#map_canvas_search')[0], lat, lng);
		});

	} else {
	    // Fallback for no geolocation
	    console.log('geoloc not shared');
	    buildMap($('#map_canvas_search')[0], lat, lng);
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
	$( ".datepicker" ).datepicker({dateFormat: 'yy-mm-dd'});
}

function resultsLoad(){}

// Load search bar
$(function(){
	var today_date = Date();
	
	$('.sun_submit').on('click', function() { 
		$('#layout_body_container').hide();
		$("#spinner").show() 
	});

	if (document.getElementById('index_form_load')){
		console.log('index load');
		var current_date = Date();

		$('#index_date').val(today_date);
		console.log($('#index_date').val());

		typeahead();
		datepicker();
		indexLoadMap();

	}else{
		console.log('not index');
		$('#sun_finder_title').show();
		resultsLoad();
		$.ajax({
			url: "form_top_partial",
			success: function(data) { 
				$('#top_form_load').append(data); 
				if (lastSearchLocation) {
					buildMap($('#map_canvas_search')[0], lastSearchLocation.lat, lastSearchLocation.lng);
					buildMap($('#map_canvas_results')[0], lastSearchLocation.lat, lastSearchLocation.lng);
				}		
				typeahead();
				datepicker();

				$('#top_date').val(today_date);
				console.log($('#top_date').val());

			},
			dataType: 'html'
		});

	}	

});

