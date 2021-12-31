// Create custom map style here: https://mapstyle.withgoogle.com/
$(document).ready(function () {
	var mapStyles = [
		{
			featureType: "administrative",
			elementType: "labels.text.fill",
			stylers: [
				{
					color: "#444444",
				},
			],
		},
		{
			featureType: "landscape",
			elementType: "all",
			stylers: [
				{
					color: "#f2f2f2",
				},
			],
		},
		{
			featureType: "poi",
			elementType: "all",
			stylers: [
				{
					visibility: "off",
				},
			],
		},
		{
			featureType: "road",
			elementType: "all",
			stylers: [
				{
					saturation: -100,
				},
				{
					lightness: 45,
				},
			],
		},
		{
			featureType: "road.highway",
			elementType: "all",
			stylers: [
				{
					visibility: "simplified",
				},
			],
		},
		{
			featureType: "road.arterial",
			elementType: "labels.icon",
			stylers: [
				{
					visibility: "off",
				},
			],
		},
		{
			featureType: "transit",
			elementType: "all",
			stylers: [
				{
					visibility: "off",
				},
			],
		},
		{
			featureType: "water",
			elementType: "all",
			stylers: [
				{
					color: "#46bcec",
				},
				{
					visibility: "on",
				},
			],
		},
		{
			featureType: "water",
			elementType: "geometry.fill",
			stylers: [
				{
					color: "#2196f3",
				},
			],
		},
	];

	/*======== 1. MAP FOR HOME PAGE ========*/

	// var mapId = document.getElementById("map-canvas");
	// if (mapId) {
	// 	/*
	//   Path to json file that contains listing data for the marker. Make sure you are calling this file through a server.
	//    */
	// 	var mapListingUrl = "assets/data/listings.json";

	// 	// map center
	// 	var center = new google.maps.LatLng(-33.924351, 151.156788);

	// 	//Map initialize function
	// 	function initialize() {
	// 		var mapOptions = {
	// 			center: center,
	// 			zoom: 15,
	// 			mapTypeId: google.maps.MapTypeId.ROADMAP,
	// 			styles: mapStyles,
	// 			scrollwheel: false,
	// 		};
	// 		//create a google map instance into the Dom element
	// 		var map = new google.maps.Map(mapId, mapOptions);

	// 		// define the format of the file retrive from server. here it is in JSON format
	// 		var mapdata = {
	// 			format: "json",
	// 		};

	// 		// the ajax callback function. Do all the stuff you want to do with the remote data in between this function.
	// 		function getContent(data) {
	// 			var markers = [];
	// 			//loop through each of the single JSON object obtained from the JSON file.

	// 			var infobox = new InfoBox({
	// 				content: "",
	// 				maxWidth: 0,
	// 				pixelOffset: new google.maps.Size(-135, -45),
	// 				zIndex: null,
	// 				closeBoxURL: "",
	// 				infoBoxClearance: new google.maps.Size(1, 1),
	// 				isHidden: false,
	// 				isOpen: false,
	// 				pane: "floatPane",
	// 				enableEventPropagation: true,
	// 				disableAutoPan: true,
	// 				alignBottom: true,
	// 			});

	// 			$.each(data, function (i, item) {
	// 				var markerCenter = new google.maps.LatLng(item.lat, item.lng);

	// 				var verified = "";

	// 				if (item.verified) {
	// 					verified = '<div class="marker-verified"><i class="fa fa-check"></i></div>';
	// 				}

	// 				var markerContent =
	// 					'<div id="marker-' +
	// 					item.id +
	// 					'" data-id="' +
	// 					item.id +
	// 					'" class="flip-container">' +
	// 					verified +
	// 					'<div class="flipper">' +
	// 					'<div class="front">' +
	// 					'<img src="' +
	// 					item.thumbnail +
	// 					'">' +
	// 					"</div>" +
	// 					'<div class="back">' +
	// 					'<i class="fa fa-eye"></i>' +
	// 					"</div>" +
	// 					"</div>" +
	// 					"</div>";

	// 				var marker = new RichMarker({
	// 					id: item.id,
	// 					data: item,
	// 					flat: true,
	// 					position: markerCenter,
	// 					map: map,
	// 					shadow: 0,
	// 					content: markerContent,
	// 					title: "Marker Title",
	// 					is_logged_in: item.is_logged_in,
	// 				});
	// 				markers.push(marker);

	// 				var infoboxTimeout;

	// 				google.maps.event.addListener(marker, "mouseover", function () {
	// 					var infoboxContent =
	// 						'<a class="list-link" href="listing-event.html">' +
	// 						'<div id="iw-container" style="background-image: url(' +
	// 						marker.data.thumbnail +
	// 						');">' +
	// 						'<div class="iw-content">' +
	// 						'<ul class="list-inline rating">' +
	// 						'<li><i class="fa fa-star" aria-hidden="true"></i></li>' +
	// 						'<li><i class="fa fa-star" aria-hidden="true"></i></li>' +
	// 						'<li><i class="fa fa-star" aria-hidden="true"></i></li>' +
	// 						'<li><i class="fa fa-star" aria-hidden="true"></i></li>' +
	// 						'<li><i class="fa fa-star" aria-hidden="true"></i></li>' +
	// 						"</ul>" +
	// 						'<div class="iw-subTitle">' +
	// 						marker.data.title +
	// 						"</div>" +
	// 						"<p>" +
	// 						marker.data.address +
	// 						"</p>" +
	// 						"</div>" +
	// 						'<div class="iw-bottom-gradient"></div>' +
	// 						"</div>" +
	// 						"</a>";

	// 					clearTimeout(infoboxTimeout);
	// 					infobox.setContent(infoboxContent);
	// 					infobox.open(map, this);
	// 					infobox.isOpen = true;
	// 				});

	// 				// hide the infowindow when user mouses-out
	// 				google.maps.event.addListener(marker, "mouseout", function () {
	// 					infoboxTimeout = setTimeout(function () {
	// 						infobox.close(map, this);
	// 						infobox.isOpen = false;
	// 					}, 150);
	// 				});

	// 				// Mouseout only for list item (Custom Event)
	// 				google.maps.event.addListener(marker, "mouseoutForList", function () {
	// 					if (infobox.isOpen) {
	// 						infobox.close(map, this);
	// 						infobox.isOpen = false;
	// 					}
	// 				});

	// 				// Event for hovering on infobox
	// 				google.maps.event.addListener(infobox, "domready", function (e) {
	// 					$(".infoBox")
	// 						.on("mouseenter", function (e) {
	// 							clearTimeout(infoboxTimeout);
	// 						})
	// 						.on("mouseleave", function (e) {
	// 							clearTimeout(infoboxTimeout);
	// 							infobox.close();
	// 						});
	// 				});
	// 			});

	// 			//Marker Cluster
	// 			var markerCluster = new MarkerClusterer(map, markers, {
	// 				imagePath: "https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m",
	// 				gridSize: 60,
	// 				maxZoom: 16,
	// 			});
	// 		}

	// 		// call the jquery ajax function
	// 		$.getJSON(mapListingUrl, mapdata, getContent);
	// 	} // map initialize function ends

	// 	var existId = document.getElementById("map-canvas");
	// 	if (existId) {
	// 		google.maps.event.addDomListener(window, "load", initialize);
	// 	}
	// }

	/*======== 2. LISTING MAIN MAP ========*/

	// var MapMain = document.getElementById("listing-main-map");
	// if (MapMain) {
	// 	// map center
	// 	var center = new google.maps.LatLng(-33.924351, 151.156788);

	// 	//Map initialize function
	// 	function initialize() {
	// 		var mapOptions = {
	// 			center: center,
	// 			zoom: 15,
	// 			mapTypeId: google.maps.MapTypeId.ROADMAP,
	// 			styles: mapStyles,
	// 			scrollwheel: false,
	// 		};
	// 		//create a google map instance into the Dom element
	// 		var map = new google.maps.Map(MapMain, mapOptions);

	// 		// the ajax callback function. Do all the stuff you want to do with the remote data in between this function.
	// 		function getContent() {
	// 			var markers = [];
	// 			//loop through each of the single JSON object obtained from the JSON file.

	// 			var infobox = new InfoBox({
	// 				content: "",
	// 				maxWidth: 0,
	// 				pixelOffset: new google.maps.Size(-135, -45),
	// 				zIndex: null,
	// 				closeBoxURL: "",
	// 				infoBoxClearance: new google.maps.Size(1, 1),
	// 				isHidden: false,
	// 				isOpen: false,
	// 				pane: "floatPane",
	// 				enableEventPropagation: true,
	// 				disableAutoPan: true,
	// 				alignBottom: true,
	// 			});

	// 			const card = $(".card-listing");
	// 			const imgs = card.find(".listing-img");
	// 			const titles = card.find(".listing-title");
	// 			const addressess = card.find(".listing-address");

	// 			for (let i = 0; i < card.length; i++) {
	// 				const lat = card[i].dataset.lat;
	// 				const lag = card[i].dataset.lag;
	// 				const id = card[i].dataset.id;
	// 				const imges = imgs[i].getAttribute("src");
	// 				const title = titles[i].textContent;
	// 				const address = addressess[i].textContent;
	// 				const checkVerified = card[i].dataset.varified;

	// 				var markerCenter = new google.maps.LatLng(lat, lag);
	// 				var verified = "";

	// 				if (checkVerified) {
	// 					verified += '<div class="marker-verified"><i class="fa fa-check"></i></div>';
	// 				}

	// 				var markerContent =
	// 					'<div id="marker" data-id="' +
	// 					id +
	// 					'" class="flip-container">' +
	// 					verified +
	// 					'<div class="flipper">' +
	// 					'<div class="front">' +
	// 					'<img src="' +
	// 					imges +
	// 					'">' +
	// 					"</div>" +
	// 					'<div class="back">' +
	// 					'<i class="fa fa-eye"></i>' +
	// 					"</div>" +
	// 					"</div>" +
	// 					"</div>";

	// 				var marker = new RichMarker({
	// 					id: id,
	// 					data: i,
	// 					flat: true,
	// 					position: markerCenter,
	// 					map: map,
	// 					shadow: 0,
	// 					content: markerContent,
	// 					title: "Marker Title",
	// 					// is_logged_in: item.is_logged_in
	// 				});
	// 				markers.push(marker);

	// 				var infoboxTimeout;

	// 				google.maps.event.addListener(marker, "mouseover", function () {
	// 					var infoboxContent =
	// 						'<a class="list-link" href="listing-event.html">' +
	// 						'<div id="iw-container" style="background-image: url(' +
	// 						imges +
	// 						');">' +
	// 						'<div class="iw-content">' +
	// 						'<ul class="list-inline rating">' +
	// 						'<li><i class="fa fa-star" aria-hidden="true"></i></li>' +
	// 						'<li><i class="fa fa-star" aria-hidden="true"></i></li>' +
	// 						'<li><i class="fa fa-star" aria-hidden="true"></i></li>' +
	// 						'<li><i class="fa fa-star" aria-hidden="true"></i></li>' +
	// 						'<li><i class="fa fa-star" aria-hidden="true"></i></li>' +
	// 						"</ul>" +
	// 						'<div class="iw-subTitle">' +
	// 						title +
	// 						"</div>" +
	// 						"<p>" +
	// 						address +
	// 						"</p>" +
	// 						"</div>" +
	// 						'<div class="iw-bottom-gradient"></div>' +
	// 						"</div>" +
	// 						"</a>";

	// 					clearTimeout(infoboxTimeout);
	// 					infobox.setContent(infoboxContent);
	// 					infobox.open(map, this);
	// 					infobox.isOpen = true;
	// 				});

	// 				// hide the infowindow when user mouses-out
	// 				google.maps.event.addListener(marker, "mouseout", function () {
	// 					infoboxTimeout = setTimeout(function () {
	// 						infobox.close(map, this);
	// 						infobox.isOpen = false;
	// 					}, 150);
	// 				});

	// 				// Mouseout only for list item (Custom Event)
	// 				google.maps.event.addListener(marker, "mouseoutForList", function () {
	// 					if (infobox.isOpen) {
	// 						infobox.close(map, this);
	// 						infobox.isOpen = false;
	// 					}
	// 				});

	// 				// Event for hovering on infobox
	// 				google.maps.event.addListener(infobox, "domready", function (e) {
	// 					$(".infoBox")
	// 						.on("mouseenter", function (e) {
	// 							clearTimeout(infoboxTimeout);
	// 						})
	// 						.on("mouseleave", function (e) {
	// 							clearTimeout(infoboxTimeout);
	// 							infobox.close();
	// 						});
	// 				});
	// 			}

	// 			//Marker Cluster
	// 			var markerCluster = new MarkerClusterer(map, markers, {
	// 				imagePath: "https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m",
	// 				gridSize: 60,
	// 				maxZoom: 16,
	// 			});

	// 			//When mouseenter into list item
	// 			$(".card-listing").on("mouseenter", function () {
	// 				var idd = $(this).attr("data-id");
	// 				$(".map-container #marker-" + idd).toggleClass("hover");

	// 				var markerHovered = markers.filter((item) => {
	// 					return item.id == idd;
	// 				})[0];

	// 				google.maps.event.trigger(markerHovered, "mouseover");
	// 			});

	// 			//When mouseleave from list item
	// 			$(".card-listing").on("mouseleave", function () {
	// 				var idd = $(this).attr("data-id");
	// 				$(".map-container #marker-" + idd).toggleClass("hover");

	// 				var markerHovered = markers.filter((item) => {
	// 					return item.id == idd;
	// 				})[0];
	// 				google.maps.event.trigger(markerHovered, "mouseoutForList");
	// 			});
	// 		}

	// 		getContent();
	// 	}
	// 	initialize();
	// }

	/*======== 3. MAP ADD OR EDIT ========*/

	// var mapAddEdit = document.getElementById("map-add-edit");
	// if (mapAddEdit) {
	// 	function initAutocomplete() {
	// 		var map = new google.maps.Map(mapAddEdit, {
	// 			center: { lat: -33.8688, lng: 151.2195 },
	// 			zoom: 13,
	// 			scrollwheel: false,
	// 			mapTypeId: "roadmap",
	// 		});

	// 		// Create the search box and link it to the UI element.
	// 		var input = document.getElementById("listingAddress");
	// 		var searchBox = new google.maps.places.SearchBox(input);
	// 		map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

	// 		// Bias the SearchBox results towards current map's viewport.
	// 		map.addListener("bounds_changed", function () {
	// 			searchBox.setBounds(map.getBounds());
	// 		});

	// 		var markers = [];
	// 		// Listen for the event fired when the user selects a prediction and retrieve
	// 		// more details for that place.
	// 		searchBox.addListener("places_changed", function () {
	// 			var places = searchBox.getPlaces();

	// 			if (places.length == 0) {
	// 				return;
	// 			}

	// 			// Clear out the old markers.
	// 			markers.forEach(function (marker) {
	// 				marker.setMap(null);
	// 			});
	// 			markers = [];

	// 			// For each place, get the icon, name and location.
	// 			var bounds = new google.maps.LatLngBounds();
	// 			places.forEach(function (place) {
	// 				if (!place.geometry) {
	// 					console.log("Returned place contains no geometry");
	// 					return;
	// 				}
	// 				var icon = {
	// 					url: place.icon,
	// 					size: new google.maps.Size(71, 71),
	// 					origin: new google.maps.Point(0, 0),
	// 					anchor: new google.maps.Point(17, 34),
	// 					scaledSize: new google.maps.Size(25, 25),
	// 				};

	// 				// Create a marker for each place.
	// 				markers.push(
	// 					new google.maps.Marker({
	// 						map: map,
	// 						icon: icon,
	// 						title: place.name,
	// 						position: place.geometry.location,
	// 					})
	// 				);

	// 				if (place.geometry.viewport) {
	// 					// Only geocodes have viewport.
	// 					bounds.union(place.geometry.viewport);
	// 				} else {
	// 					bounds.extend(place.geometry.location);
	// 				}
	// 			});
	// 			map.fitBounds(bounds);
	// 		});

	// 		google.maps.event.addListener(map, "click", function (event) {
	// 			placeMarker(event.latLng);
	// 		});

	// 		function placeMarker(location) {
	// 			if (typeof marker == "undefined") {
	// 				marker = new google.maps.Marker({
	// 					position: location,
	// 					map: map,
	// 					animation: google.maps.Animation.DROP,
	// 				});
	// 			} else {
	// 				marker.setPosition(location);
	// 			}

	// 			//Set data-location attribute for marker location
	// 			input.setAttribute("data-location", location);
	// 			document.getElementById("location").innerHTML = location;
	// 		}
	// 	}
	// 	google.maps.event.addDomListener(window, "load", initAutocomplete);
	// }

	/*======== 4. MAP ADD OR EDIT ========*/

	var listingSingleMap = document.getElementById("single-listing-map");
	if (listingSingleMap) {
		function initialize() {
			var lat = parseFloat(listingSingleMap.dataset.lat);
			var lag = parseFloat(listingSingleMap.dataset.lag);

			//
			var address = GetFormattedAddressFromCoordinates(lat, lag).then(
				function (address) {
					console.log(address);
					var spnFullAddress = document.getElementById("spnFullAddress");
					if (listingSingleMap) {
						spnFullAddress.innerHTML = address;
					}
				}
			);
			

			var map_options = {
				disableDefaultUI: false,
				center: new google.maps.LatLng(lat, lag),
				zoom: 14,
				scrollwheel: true,
				zoomControl: true,
				streetViewControl: false,
				mapTypeControl: false,
				fullscreenControl: false,
				styles: mapStyles,
			};

			var map = new google.maps.Map(listingSingleMap, map_options);
			var marker = new google.maps.Marker({
				map: map,
				position: new google.maps.LatLng(lat, lag),
				title: "Title",
			});
			var info = new google.maps.InfoWindow({
				content: "marker content",
			});

			google.maps.event.addListener(marker, "click", function () {
				info.open(map, marker);
			});
			var gotoMapButton = document.createElement("div");
			gotoMapButton.setAttribute("class", "btn-map-view");
			gotoMapButton.innerHTML = "Get Directions";
			map.controls[google.maps.ControlPosition.TOP_LEFT].push(gotoMapButton);

			google.maps.event.addDomListener(gotoMapButton, "click", function () {
				// you can also hard code the URL ,
				var url = "https://www.google.com/maps/dir/?api=1&destination=" + lat + "," + lag;

				window.open(url);
			});
		}
		google.maps.event.addDomListener(window, "load", initialize);
		// if (document.readyState === "complete") {
		//   google.maps.event.addDomListener(window, "load", initialize);
		// }
	}

	/*======== 4. MAP SIMPlE ========*/

	// var contactUsMap = document.getElementById("simple-map");
	// if (contactUsMap) {
	// 	var marker;

	// 	function initMap() {
	// 		var map = new google.maps.Map(contactUsMap, {
	// 			zoom: 16,
	// 			scrollwheel: false,
	// 			styles: mapStyles,
	// 			center: { lat: 40.80333012, lng: -73.959329496 },
	// 		});

	// 		marker = new google.maps.Marker({
	// 			map: map,
	// 			draggable: true,
	// 			animation: google.maps.Animation.BOUNCE,
	// 			position: { lat: 40.80333012, lng: -73.959329496 },
	// 		});
	// 	}

	// 	initMap();
	// }

	/*======== 5. SELECT COORDINATES MAP ========*/
	var selectCoordinatesMap = document.getElementById("select-coordinates-map");
	if (selectCoordinatesMap) {
		function initMapSelectCoordinates() {
			// Middle of the US coord.
			//const middleOfUSLatlng = { lat: 41.31519478310302, lng: -97.62826822821022 };

			var lat = parseFloat(selectCoordinatesMap.dataset.lat);
			var lag = parseFloat(selectCoordinatesMap.dataset.lag);

			// If no coordinates provides, point to middle of US.
			if (!lat) {
				lat = 41.31519478310302;
			}
			if (!lag) {
				lag = -97.62826822821022;
			}

			const myLatlng = { lat: lat, lng: lag };

			var map_options = {
				disableDefaultUI: false,
				center: myLatlng,
				zoom: 14,
				scrollwheel: true,
				zoomControl: true,
				streetViewControl: false,
				mapTypeControl: false,
				fullscreenControl: false,
				styles: mapStyles,
			};

			var map = new google.maps.Map(selectCoordinatesMap, map_options);

			// Create the initial InfoWindow.
			let infoWindow = new google.maps.InfoWindow({
				content: "Click the map to get Lat/Lng!",
				position: myLatlng,
			});

			infoWindow.open(map);

			// Configure the click listener.
			map.addListener("click", (mapsMouseEvent) => {
				// Close the current InfoWindow.
				infoWindow.close();

				// Create a new InfoWindow.
				infoWindow = new google.maps.InfoWindow({
					position: mapsMouseEvent.latLng,
				});

				var coordinates = mapsMouseEvent.latLng.toJSON();

				infoWindow.setContent(JSON.stringify(coordinates, null, 2));
				infoWindow.open(map);

				// Updates the Latitude and Longitude inputs with the coordinates selected.
				$("input[name=latitude]")[0].value = coordinates.lat;
				$("input[name=longitude]")[0].value = coordinates.lng;
				//console.log("Lat:" + coordinates.lat + " | " + "Lng: " + coordinates.lng);
			});
		}

		google.maps.event.addDomListener(window, "load", initMapSelectCoordinates);
	}
});

function GetFormattedAddressFromCoordinates(latitude, longitude) {
	//const input = document.getElementById("latlng").value;
	//const latlngStr = input.split(",", 2);
	const latlng = {
		lat: parseFloat(latitude),
		lng: parseFloat(longitude),
	};

	var geocoder = new google.maps.Geocoder();

	return new Promise((resolve, reject) => {
		geocoder
			.geocode({ location: latlng })
			.then((response) => {
				if (response.results[0]) {
					resolve (response.results[0].formatted_address);
				} else {
					reject(console.log("GetFormattedAddressFromCoordinates: No results found!"));
				}
			})
			.catch((e) => console.log("Geocoder failed due to: " + e));
	});
}
