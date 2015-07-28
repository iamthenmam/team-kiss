

function initialize () {

  mapCanvas = document.getElementById("map-canvas");
  var backgroundMap = new google.maps.Map(mapCanvas);

  var mapOptions = {
    center: new google.maps.LatLng(44.5403, -78.5463),
    zoom: 22,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  };
}

google.maps.event.addDomListener(window, "load", initialize);

// codeAddress('London')
