// Main Javascript file for Sun Finder


// load map of SF with central location based on search
function initialize() { 
    //stops other event listeners from firing on search button
    //event.preventDefault(); 

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

	//search result marker var
	var marker = new google.maps.Marker({
	    position: myLatlng,
		map: map,
		title: 'Hello World!'
	});

	//sample Marker with Label
	// var marker1 = new google.maps.MarkerWithLabel({
 //       position: myLatLng,
 //       draggable: true,
 //       raiseOnDrag: true,
 //       map: map,
 //       labelContent: "$425K",
 //       labelAnchor: new google.maps.Point(22, 0),
 //       labelClass: "labels", // connects to CSS class label
 //       labelStyle: {opacity: 0.75}
 //    });

 //    var iw1 = new google.maps.InfoWindow({
 //       content: "Home For Sale"
 //    });

	//put multiple markers on map
	function createMarker(position, label) {
		//FIX need to figure out how to swap out google marker with my own and get label to come up
	    return new google.maps.Marker({
		    position: position,
		    draggable: false,
		    map: map,
		    title: label,
		    labelText: label,
		    labelClass: "labels", // the CSS class for the label
		    labelStyle: {top: "0px", left: "-21px", opacity: 0.75},
		    labelVisible: true
	    });
	 }

	var readData = function() { // create markers
		pos = [
			new google.maps.LatLng(37.7627, -122.4352),
	  		new google.maps.LatLng(37.7600, -122.4148),
	  		new google.maps.LatLng(37.7572, -122.3999),
	  		new google.maps.LatLng(37.7415, -122.4144)
	  		];

		label = ["Castro", "Mission", "Potrero", "Bebo"];

		for (var i = 0; i < pos.length; i++) {
	    	createMarker(pos[i], label[i]);
	  }     
	 }

	// google automatic map layer from weather.com - doesn't provide as much detail for neighborhood but good example
	var weatherLayer = new google.maps.weather.WeatherLayer({
    	temperatureUnits: google.maps.weather.TemperatureUnit.FAHRENHEIT
  	});
  	weatherLayer.setMap(map);
    readData();
}

// $(function()){
// 	google.maps.event.addDomListener(window, 'load', initialize);	
// }
// google.maps.event.addDomListener(window, 'load', initialize);
//google.maps.event.addDomListener(searchFinder, 'click', initialize);


// google.maps.event.addListner(marker1, "click", function (e) { iwl.open(map, this); });

//autocomplete function
$(function() {
	var tags = availableTags;

	$( ".loc" ).autocomplete({
    	source: tags, minLength: 3
	});
});

// jquery search event map load - set as if there is coord then initialize
if(map_lat && map_long){
	initialize();	
};


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

