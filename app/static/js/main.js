// Main Javascript file for Sun Finder

// Confirm load
console.log("main js");

// Load search bar
$(function(){
	// $( ".page_results" ).on('load', function() {
		// console.log('check for index');
		// if ($("#index_form_load")){
			console.log('index found');
		 	// $("#index_form_load").load('sun_index_form.html'); 
			$.get('sun_index_form', function(data) {
		  		$('#index_form_load').html(data);
			});
			indexLoadMap();
		// } else 	if !($("#index_form_load")) {
	// 	console.log('not index');

	// }	
	// });
	});

// Load map  - currently SF biased
function buildMap(container, map_lat, map_long) { 

	// Pre-set lat lng to SF if not provided
	if (!map_lat || !map_long) {
		map_lat = 37.7655;
		map_long = -122.4429;
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
	console.log('index load map');
	if (navigator.geolocation) {
	    var location_timeout = setTimeout("geolocFail()", 10000);

	    navigator.geolocation.getCurrentPosition(function(position) {
	        clearTimeout(location_timeout);

	        lat = position.coords.latitude;
	        lng = position.coords.longitude;

	        console.log(lat + ' ' + lng);

	        buildMap($('#map_canvas_search')[0], lat, lng);
	    }, function(error) {
	        clearTimeout(location_timeout);
	        geolocFail();
		    console.log('geo loc not exist');
		    buildMap($('#map_canvas_search')[0]);
		});

	} else {
	    // Fallback for no geolocation
	 	geolocFail();
	    console.log('geoloc not shared');
	    buildMap($('#map_canvas_search')[0]);
	}
}

// $(document).ready(indexLoadMap);

// Typeahead - Autocomplete
function typeahead(selector) {
	console.log("typeahead"); //test

	$(selector).typeahead({
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
	$( ".datepicker" ).datepicker({dateFormat: 'yy-mm-dd'});
}


function loadTopSearch(){
	$.get('sun_top_form', function(data) {
		$('#top_form_load').html(data);
	if (lastSearchLocation) {
		buildMap($("#map_canvas_search")[0], lastSearchLocation.lat, lastSearchLocation.lng);
	}	  		
		typeahead("#sun_query")
	});

}

// Weather Search
function handleSearch(e) {

	var query = $("#sun_query").val();	

	var date = $(".sun-date").val();
	e.preventDefault(); //Prevents default form value call
	$('#spinner').show();
	$('.page_results').hide();
	$('.top-bar').show();
	console.log(query);
	$.post('search_results', { "date": date, "query": query }, function(data) {
		$('#spinner').hide();
		// $("#sun-query_top").val('');
		$('.page_results').show();
		$('.page_results').html(data);
		loadTopSearch();
		});

}



$(window).load(function(){

	$(function(){
		$(".sun_submit").on("click", handleSearch);

	});
	typeahead("#sun_query");
	datepicker();

});

// Link Load
$(function (){
 console.log('in link load');  

	$('#create_account_load').on('click', function(e){
		loadTopSearch();
		$.post('create_login', function(data){
  			$('.page_results').html(data);
  		});
	});

 
    $('#about_load').on('click', function(e){
    	loadTopSearch();
  		$.post('about', function(data){
  			$('.page_results').html(data);
  		});
  	});

	$('#privacy_load').on('click', function(e){
		loadTopSearch();
		$.post('privacy', function(data){
  			$('.page_results').html(data);
  		});
	});

	$('#tos_load').on('click', function(e){
		loadTopSearch();
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



