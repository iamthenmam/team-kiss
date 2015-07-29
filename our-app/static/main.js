// $("#hide-button").click(function() {
//   $("#results").toggle()
//
// $("#search-button").click(function() {
//   $("#results").show()


function loadScript() {
  var script = document.createElement("script");
  script.type = "text/javascript";
  script.src = "https://maps.googleapis.com/maps/api/js?" +
               "key=AIzaSyABHO66skhWRgmCmYBKGQ-XSqZpaP8AkLI&" +
               "v=3.exp&signed_in=false&callback=initialize";
  document.body.appendChild(script);
}

window.onload = loadScript;

var geocoder
var backgroundMap

function initialize() {
  var mapCanvas = document.getElementById("map-canvas");

  var mapOptions = {
    center: new google.maps.LatLng(39.8282, -98.5795),
    zoom: 4,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  };

  backgroundMap = new google.maps.Map(mapCanvas, mapOptions);
}

function codeAddress() {
  var converted_location
  var geocoder = new google.maps.Geocoder();
  var address = document.getElementById("uncoded_location").value;
  geocoder.geocode( { "address": address}, function(results, status) {
    if (status == google.maps.GeocoderStatus.OK) {
      var converted_location = results[0].geometry.location
      map.setCenter(converted_location);
    } else {
      alert("Geocode was not successful for the following reason: " + status);
    }
  });
  function setOutput(itsId, itsValue) {
    document.getElementById(itsId).value = itsValue;
  };
  setOutput(uncoded_location, converted_location);
}

////////////////////////////////////////////////////////////////////////////////
