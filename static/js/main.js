// Main Javascript file for Sun Finder

//load the visualization API with the map package
// google.load("visualization", "1", {packages: ["map"]});

// load map of SF with central location based on search
function initialize() {
	//var myLatLng = map_lat,map_long
	var myLatlng = new google.maps.LatLng(map_lat,map_long);
	var map_canvas = document.getElementById('map_canvas');
	var map_options = {
	  // center: new google.maps.LatLng(37.7655,-122.4429),
	  center: myLatlng,
	  zoom: 13,
	  mapTypeId: google.maps.MapTypeId.ROADMAP
	}
	
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

	var marker = new google.maps.Marker({
	    position: myLatlng,
		map: map,
		title: 'Hello World!'
	});

	//put markers on map
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

	 // 	return new MarkerWithLabel({
		//    position: position,
		//    draggable: false,
		//    map: map,
		//    labelContent: "$425K",
		//    labelAnchor: new google.maps.Point(22, 0),
		//    labelClass: "labels", // the CSS class for the label
		//    labelStyle: {opacity: 0.75}
		//  });

	 // }

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

google.maps.event.addDomListener(window, 'load', initialize);

//ajax loader
function ajaxCall(){
    $("#LoadingImage").show();

      $.ajax({ 
      type: "GET", 
      url: surl, 
      dataType: "jsonp", 
      cache : false, 
      jsonp : "onJSONPLoad", 
      jsonpCallback: "newarticlescallback", 
      crossDomain: "true", 
      success: function(response) { 
        $.("#LoadingImage").hide();
        alert("Success"); 
      }, 
      error: function (xhr, status) {  
        $.("#LoadingImage").hide();
        alert('Unknown error ' + status); 
      }    
   });  
} 
