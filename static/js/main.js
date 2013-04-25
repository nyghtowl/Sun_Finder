// Main Javascript file for Sun Finder

//load the visualization API with the columnchart package
google.load("visualization", "1", {packages: ["columnchart"]});

	      function initialize() {
	        var map_canvas = document.getElementById('map_canvas');
	        var map_options = {
	          center: new google.maps.LatLng(37.7655,-122.4429),
	          zoom: 12,
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
	          }
	        ]);

	      }
	      