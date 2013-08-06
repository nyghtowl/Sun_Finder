// Main Javascript file for Sun Finder

// Confirm load
console.log("main js");

// Load map  - currently SF biased
function buildMap(map_lat, map_long) { 
	// Pre-set lat lng to SF if not provided
	if (!map_lat || !map_long) {
		map_lat = 37.7655;
		map_lng = -122.4429
	}
    //stops other event listeners from firing on search button
    //event.preventDefault(); 	
	console.log("build_map"); // test
	
	//Pulls lat, lng from search result
	var myLatlng = new google.maps.LatLng(map_lat,map_long);
	var map_options = {
	  // center: new google.maps.LatLng(37.7655,-122.4429),
	  center: myLatlng,
	  zoom: 13,
	  mapTypeId: google.maps.MapTypeId.ROADMAP
	}
	
	// Establishes Google maps
	var map = new google.maps.Map($("#map_canvas_search")[0], map_options)
	
	// Map style - move to css?
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

	singleMapMark(map);
    mutipleMapMarks(map, myLatlng);

  	// weatherOverlay(map); - not detailed enough but similar concept

}


function singleMapMark(map, myLatlng){
	// Search result marker - custom img and marker variable
	var img_map = {
		scaledSize: new google.maps.Size(20, 25),
		size: new google.maps.Size(25, 32),
		url: "http://maps.gstatic.com/mapfiles/icon_green.png",
	};

	var marker = new google.maps.Marker({
	    position: myLatlng,
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

// Add Google automatic weather overlay - not detailed enough
function weatherOverlay(map){
	// Google automatic map layer from weather.com - doesn't provide as much detail for neighborhood but good example
	var weatherLayer = new google.maps.weather.WeatherLayer({
    	temperatureUnits: google.maps.weather.TemperatureUnit.FAHRENHEIT
      	});
	weatherLayer.setMap(map);
}


// Build map index initializer
function indexLoadMap(){
	if (navigator.geolocation) {
	    var location_timeout = setTimeout("geolocFail()", 10000);

	    navigator.geolocation.getCurrentPosition(function(position) {
	        clearTimeout(location_timeout);

	        lat = position.coords.latitude;
	        lng = position.coords.longitude;

	        console.log(lat + ' ' + lng);
	        buildMap(lat, lng);
	    }, function(error) {
	        clearTimeout(location_timeout);
	        geolocFail();
		    console.log('geo loc not exist');
		    buildMap(lat, lng);
		});

	} else {
	    // Fallback for no geolocation
	 	geolocFail();
	    console.log('geoloc not shared');
	    buildMap(lat, lng);
	}
}

$(document).ready(indexReady);


// Typeahead - Autocomplete
$(function() {
	console.log("typeahead"); //test

	$("#sun_query_index, #sun_query_top").typeahead({
	    minLength: 2,
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

});

// Datepicker
$(function() {
	$( ".datepicker" ).datepicker({dateFormat: 'yy-mm-dd'});
});

// Weather Search
$(function(){
	$(".sun-submit").on("click", handleSearch);

});

function handleSearch(e) {
	if ($("#sun_query_index").val()) {
		var query = $("#sun_query_index").val();	
	} else if ($("#sun_query_top").val()) {
		var query = $("#sun_query_top").val();
	}
	var date = $(".sun-date").val();
	e.preventDefault(); //Prevents default form value call
	$('#spinner').show();
	$('.page_results').hide();
	$('.top-bar').show();
	console.log(query);
	$.post('search_results', { "date": date, "query": query }, function(data) {
		$('#spinner').hide();
		$("#sun-query2").val('');
		$('.page_results').show();
		$('.page_results').html(data);

	});

}



// Footer Link Load
$(function (){
 console.log('in footer link load');  
 
    $('#about_load').on('click', function(e){
    	$('.top-bar').show();
  		$.post('about', function(data){
  			$('.page_results').html(data);
  		});
  	});

	$('#privacy_load').on('click', function(e){
		$('.top-bar').show();
		$.post('privacy', function(data){
  			$('.page_results').html(data);
  		});
	});

	$('#tos_load').on('click', function(e){
		$('.top-bar').show();
		$.post('tos', function(data){
  			$('.page_results').html(data);
  		});
	});

});


// $(function(){
// 	$('#buid-map').on('click', build_map(37.7655,-122.4429));
// });


// run spinner
// function loadSubmit() {
// 	ProgressImage = document.getElementById(’progress_image’);
// 	document.getElementById(”progress”).style.visibility = “visible”;
// 	setTimeout(”ProgressImage.src = ProgressImage.src”,100);
// 	return true;
// }

// FIX - jquery to run the spinner and post the results page
// $.ajax({
//   type: "POST",
//   url: url,
//   data: data,
//   success: success,
//   dataType: dataType
// });

// $.post('ajax/test.html', function(data) {
//   $('.result').html(data);
// });



