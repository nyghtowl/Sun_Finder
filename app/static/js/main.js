// Main Javascript file for Sun Finder

// Confirm load
console.log("main js");


// Load map  - currently SF biased
function buildMap(map_lat, map_long) { 

	console.log("build map");
	// Pre-set lat lng to SF if not provided
	if (!map_lat || !map_long) {
		map_lat = 37.7655;
		map_long = -122.4429;
	}
    //stops other event listeners from firing on search button
	console.log("build_map" + map_lat); // test
	
	//Pulls lat, lng from search result
	// var myLatLng = new google.maps.LatLng(map_lat,map_long);
	// var map_options = {
	//   // center: new google.maps.LatLng(37.7655,-122.4429),
	//   center: myLatLng,
	//   zoom: 13,
	//   mapTypeId: google.maps.MapTypeId.ROADMAP
	// }
	
	// Establishes Google maps
	// var map = new google.maps.Map(container, map_options)
	

	var map = new GMaps({
	  div: '#map_canvas_search',
	  lat: map_lat,
	  lng: map_long,
	  zoom: 13
	});

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

	// singleMapMark2(map, map_lat, map_long);
	// drawOverlay(map, map_lat, map_long)
	// singleMapMark(map, myLatLng);
 //    mutipleMapMarks(map);

}

function singleMapMark2(map, map_lat, map_long){
	map.addMarker({
		lat: map_lat,
		lng: map_long,
		title: 'Search Result',
		url: "http://maps.gstatic.com/mapfiles/icon_green.png",

	  	click: function(e) {
	    	alert('Sun Search Location');
	  }
	});
}

function drawOverlay(map, map_lat, map_long){
	map.drawOverlay({
	lat: map_lat,
	lng: map_long,
	content: '<a href="http://nyghtowl.io">Mission</a>'
});
}

function geoLocate(map){
	GMaps.geolocate({
	  success: function(position) {
	    map.setCenter(position.coords.latitude, position.coords.longitude);
	  },
	  error: function(error) {
	    alert('Geolocation failed');
	  },
	  not_supported: function() {
	    alert("Your browser does not support geolocation");
	  },
	  always: function() {
	    alert("Done!");
	  }
	});
}

function singleMapMark(map, myLatLng){
	// Search result marker - custom img and marker variable
	var img_map = {
		scaledSize: new google.maps.Size(20, 25),
		size: new google.maps.Size(25, 32),
		url: "http://maps.gstatic.com/mapfiles/icon_green.png",
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
		url:'/map_details',
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

	        buildMap(lat, lng);
	    }, function(error) {
		    console.log('geo loc not exist');
	        buildMap(lat, lng);
		});

	} else {
	    // Fallback for no geolocation
	    console.log('geoloc not shared');
	    buildMap(lat, lng);
	}
}

// function handleSearch(e) {
// 	$.ajax({
// 		type: "POST",
// 		url:'/search_results_partial',
// 		data: { "date": date, "query": query },
// 		cache: false,
// 		processData: false,
// 		dataType: "html"
// 	}).done(function(html){
// 		$('.page_results').append(html);
// 	});

// }


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


// Load search bar
$(function(){

	$('.sun_submit').on('click', function() { 
		$('#layout_body_container').hide();
		$("#spinner").show() 
	});

	if (document.getElementById('index_form_load')){
		console.log('index load');
		typeahead();
		datepicker();
		indexLoadMap();
	}else{
		console.log('not index');
		$('#sun_finder_title').show();
		$.get('form_top_partial', function(data) {
			$('#top_form_load').html(data);
			alert(lastSearchLocation.lat);	
			if (lastSearchLocation) {
				buildMap(lastSearchLocation.lat, lastSearchLocation.lng);
			}	  		
			typeahead();
			datepicker();
		});	
	}	

});

