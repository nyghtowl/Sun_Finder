// Main Javascript file for Sun Finder


// load map of SF with central location based on search
function initialize() { 
    //stops other event listeners from firing on search button
    //event.preventDefault(); 
console.log("initialize");
	//pulls lat, lng from fast result html
	var myLatlng = new google.maps.LatLng(map_lat,map_long);
	var map_canvas = document.getElementById('map_canvas');
	var map_options = {
	  // center: new google.maps.LatLng(37.7655,-122.4429),
	  center: myLatlng,
	  zoom: 13,
	  mapTypeId: google.maps.MapTypeId.ROADMAP
	}
	
	//map var
	var map = new google.maps.Map(map_canvas, map_options)
	
	// set map style
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

	//search result marker - custom img and marker variable
	var img_map = {
		scaledSize: new google.maps.Size(20, 25),
		size: new google.maps.Size(25, 32),
		url: "http://maps.gstatic.com/mapfiles/icon_green.png",
	};


	var marker = new google.maps.Marker({
	    position: myLatlng,
		map: map,
		// icon: "http://maps.gstatic.com/mapfiles/icon_green.png",
		icon: img_map,
		title: "Sun Search"
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

	//put multiple markers on map
	// function createMarker(position, label) {
	// // 	//FIX need to figure out how to swap out google marker with my own and get label to come up
	//     return new google.maps.Marker({
	// 	    position: position,
	// 	    draggable: false,
	// 	    map: map,
	// 	    title: label,
	// 	    labelText: label,
	// 	    labelClass: "labels", // the CSS class for the label
	// 	    labelStyle: {top: "0px", left: "-21px", opacity: 0.75},
	// 	    labelVisible: true
	//     });
	//  }

	// apply MarkerWith Label to putting multiple markers on the map
	function createMarker(position, label) {
		return new MarkerWithLabel({
	       position: position,
	       draggable: false,
	       raiseOnDrag: false,
	       map: map,
	       labelContent: label,
	       labelAnchor: new google.maps.Point(22, 0),
	       labelClass: "labels", // connects to CSS class label
	       labelStyle: {opacity: 1}
    	});
	}


	var readData = function(positions, labels) { // create markers

// //FIX passing variables from html to js - can this be rewritten in JQuery - use commented out version to get it to work again
		for (var i = 0; i < positions.length; i++) {
	    	createMarker(positions[i], labels[i]);
	  	}     
	 }

	// google automatic map layer from weather.com - doesn't provide as much detail for neighborhood but good example
	var weatherLayer = new google.maps.weather.WeatherLayer({
    	temperatureUnits: google.maps.weather.TemperatureUnit.FAHRENHEIT
  	});

  	//loads weather layer
  	// weatherLayer.setMap(map);

  	//adds static markers based on lat, long
    readData(positionCoords, availableTags);

	// var positions = [
	//   		new google.maps.LatLng(37.7600, -122.4148),
	//   		new google.maps.LatLng(37.7572, -122.3999),
	//   		new google.maps.LatLng(37.7415, -122.4144)
	// ];
	// var labels = ["Mission", "Potrero", "Bubo"];
	// readData(positions, labels);


	// google.maps.event.addListener(marker1, "click", function (e) { iw1.open(map, this); });	

}

console.log("main immediate");
// previous approach call the map load function
// 	google.maps.event.addDomListener(window, 'load', initialize);	

//starting a jquery example that pulls the variables from html
// $(function(){

// 	var pos = positionCoords;
//  	var label = availableTags;

// });

// jquery search event map load - set as if there is coord then initialize
$(function() { 
	if(map_lat && map_long){
		initialize();
	};
})


// $(document).ready(function() {....})

// jquery autocomplete function
$(function() {
console.log("anon autocomplete");
	var tags = availableTags;

	$( ".loc" ).autocomplete({
    	source: tags, minLength: 1
	});
});

//datepicker
$(function() {
		$( ".datepicker" ).datepicker({dateFormat: 'yy-mm-dd'});
	});


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

			// $(function(){
			// 	google.maps.event.addDomListener(window, 'load', initialize);
			// }
//$('body').on('load', initialize);

//FIX - ajax loader

// Liz version of code - need to recreate results pg to be generated by js
// function makeLoaderBar(ln) {
//     $('body').html($('<div class="progress progress-striped active"><div class="bar" style="width: '+ln+'%;"></div></div>'))
// }

// $.getJSON('/some_json_route', function(data) {
//   console.log(data);
// });

// ex code pulled off internet
// function ajaxCall(){
//     $("#LoadingImage").show();

//       $.ajax({ 
//       type: "GET", 
//       url: surl, 
//       dataType: "jsonp", 
//       cache : false, 
//       jsonp : "onJSONPLoad", 
//       jsonpCallback: "newarticlescallback", 
//       crossDomain: "true", 
//       success: function(response) { 
//         $.("#LoadingImage").hide();
//         alert("Success"); 
//       }, 
//       error: function (xhr, status) {  
//         $.("#LoadingImage").hide();
//         alert('Unknown error ' + status); 
//       }    
//    });  
// } 

// $("#search_form1").on("submit", initialize);
// $("#search_form2").on("submit", initialize);

