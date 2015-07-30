$("#toggleButton").click(function() {
  $("#results").slideToggle(250);
});

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
    center: new google.maps.LatLng(window.location_searched.loc_lat, window.location_searched.loc_lng),
    zoom: window.location_searched.loc_zoom,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  };

  var backgroundMap = new google.maps.Map(mapCanvas, mapOptions);

  function placeMarker(marker, searched) {
    var location = new google.maps.LatLng(marker.lat,marker.lng);

    var pinColor = "";
    function getRandomColor() {
      var letters = '0123456789ABCDEF'.split('');
      for (var i = 0; i < 6; i++) {
          pinColor += letters[Math.floor(Math.random() * 16)];
      }
      return pinColor;
    };

    if (!searched) {
      pinColor = getRandomColor();
      var pinImage = new google.maps.MarkerImage("http://www.googlemapsmarkers.com/v1/" + pinColor + "/");
      var googleMarker = new google.maps.Marker({
          icon: pinImage,
          position: location,
          map: backgroundMap,
          title: marker.title
      });
    } else {
      var googleMarker = new google.maps.Marker({
          position: location,
          map: backgroundMap,
          title: marker.title
      });
    };

    function displayString(wordAndDef) {
      var infowindow = new google.maps.InfoWindow({
      content: wordAndDef
      });
      infowindow.open(backgroundMap, googleMarker);
    };

    google.maps.event.addListener(googleMarker, "click", function() {
      console.log("nothing wrong");
      displayString(marker.string);
    });
  };

  for (marker in window.markers) {
    var searched = false;
    window.markers[marker];
    if (window.markers[marker].title == window.searched_word) {
      searched = true;
    };
    placeMarker(window.markers[marker], searched);
  };
}
