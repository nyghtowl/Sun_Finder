// Main Javascript file for Sun Finder

// Confirm load
console.log("main js");

// Load map  - currently SF biased
function build_map(map_lat, map_long) { 
	if (!map_lat || !map_long) {
		return
	}
    //stops other event listeners from firing on search button
    //event.preventDefault(); 
console.log("build_map"); // test
	
	//Pulls lat, lng from search result
	var myLatlng = new google.maps.LatLng(map_lat,map_long);
	var map_canvas = document.getElementById('map_canvas');
	var map_options = {
	  // center: new google.maps.LatLng(37.7655,-122.4429),
	  center: myLatlng,
	  zoom: 13,
	  mapTypeId: google.maps.MapTypeId.ROADMAP
	}
	
	// Establishes Google maps
	var map = new google.maps.Map(map_canvas, map_options)
	
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

	// Search result marker - custom img and marker variable
	var img_map = {
		scaledSize: new google.maps.Size(20, 25),
		size: new google.maps.Size(25, 32),
		url: "http://maps.gstatic.com/mapfiles/icon_green.png",
	};


	var marker = new google.maps.Marker({
	    position: myLatlng,
		map: map,
		icon: img_map,
		title: "Search Result"
	});

	// var homeLatLng = new google.maps.LatLng(37.7627, -122.4352);

	// var marker1 = new MarkerWithLabel({
 //       position: new google.maps.LatLng(37.7627, -122.4352),
 //       draggable: false,
 //       raiseOnDrag: false,
 //       map: map,
 //       labelContent: "Mission",
 //       labelAnchor: new google.maps.Point(22, 0),
 //       labelClass: "labels", // connects to CSS class label
 //       labelStyle: {opacity: 1}
 //    });

	// puts a comment box over the marker
    // var iw1 = new google.maps.InfoWindow({
    //    content: "Home For Sale"
    // });


	// Apply MarkerWith Label - add multiple markers on the map
	function createMarker(position, label) {
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

	// Create multiple markers
	var readData = function(positions, labels) { 
		for (var i = 0; i < positions.length; i++) {
	    	createMarker(positions[i], labels[i]);
	  	}     
	 }

	// Google automatic map layer from weather.com - doesn't provide as much detail for neighborhood but good example
	var weatherLayer = new google.maps.weather.WeatherLayer({
    	temperatureUnits: google.maps.weather.TemperatureUnit.FAHRENHEIT
  	});

 //  	// Loads weather layer
 //  	// weatherLayer.setMap(map);

	function mark_map() {
		$.ajax({
			url:'/map_details',
			type: "GET",
			cache: false,
			dataType: "json",
			success: function(data){
				console.log(data.result.locations);
				readData(data.result.loc_coords, data.result.locations);
				}
		});
	}

    mark_map();

}



// Jquery search event map load - set as if there is coord then build_map
$(function(map_lat, map_long) { 
	build_map(map_lat, map_long);
});

// Get geolocation to set initial map
$(function() {
	// Pre-set lat lng to SF
	var lat = 37.7655;
	var lng = -122.4429

		if (navigator.geolocation) {
		    var location_timeout = setTimeout("geolocFail()", 10000);

		    navigator.geolocation.getCurrentPosition(function(position) {
		        clearTimeout(location_timeout);

		        lat = position.coords.latitude;
		        lng = position.coords.longitude;

		        console.log(lat + ' ' + lng);
		        build_map(lat, lng);

		    }, function(error) {
		        clearTimeout(location_timeout);
		        geolocFail();
			    console.log('geo loc not exist');
		        build_map(lat, lng);
		    });
		} else {
		    // Fallback for no geolocation
		 	geolocFail();
		    console.log('geoloc not shared');
		    build_map(lat, lng);
		}

});

// Typeahead - Autocomplete
$(function() {
	console.log("typeahead"); //test

	$("#sun-query1, #sun-query2").typeahead({
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
	var query = $("#sun-query1").val();
	var query2 = $("#sun-query2").val();
	var date = $(".sun-date").val();
	e.preventDefault(); //Prevents default form value call
	$('#spinner').show();
	$('.page_results').hide();
	$('.top-bar').show();
	console.log(query + '2' + query2);
	if (query) {
		$.post('search_results', { "date": date, "query": query }, function(data) {
			$('#spinner').hide();
			$('.page_results').show();
			$('.page_results').html(data);
		});
	} else if (query2) {
		$.post('search_results', { "date": date, "query": query2 }, function(data) {
			$('#spinner').hide();
			$('.page_results').show();
			$('.page_results').html(data);
		});		
	}
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

// Triggers when to run search call
// $(document).ready(dom_ready);

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



