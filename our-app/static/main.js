$("#toggleButton").click(function() {
  $("#results").slideToggle(250);
});

////////////////////////////////////////////////////////////////////////////////

function loadScript() {
  var script = document.createElement("script");
  script.type = "text/javascript";
  script.src = "https://maps.googleapis.com/maps/api/js?" +
               "key=AIzaSyABHO66skhWRgmCmYBKGQ-XSqZpaP8AkLI&" +
               "v=3.exp&signed_in=false&callback=initialize";
  document.body.appendChild(script);
}

window.onload = loadScript;


function initialize() {
  var mapCanvas = document.getElementById("map-canvas");

  var mapOptions = {
    center: new google.maps.LatLng(39.8282, -98.5795),
    zoom: 4,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  };

  var backgroundMap = new google.maps.Map(mapCanvas, mapOptions);

  function placeMarker(marker) {
    var location = new google.maps.LatLng(marker.lat,marker.lng);
    var marker = new google.maps.Marker({
        position: location,
        map: backgroundMap,
        title: marker.title
    });
  }
  for (marker in window.markers) {
    window.markers[marker];
    placeMarker(window.markers[marker]);
  };
}
