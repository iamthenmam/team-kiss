// $("results").hide();

// $("#results").click(function() {
//   $("#results").show()
// })

function initialize() {
  var mapCanvas = document.getElementById("map-canvas");

  var mapOptions = {
    center: new google.maps.LatLng(39.8282, -98.5795),
    zoom: 4,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  };

  var backgroundMap = new google.maps.Map(mapCanvas, mapOptions);

}

function loadScript() {
  var script = document.createElement('script');
  script.type = 'text/javascript';
  script.src = "https://maps.googleapis.com/maps/api/js?" +
               "key=AIzaSyABHO66skhWRgmCmYBKGQ-XSqZpaP8AkLI&" +
               "v=3.exp&signed_in=false&callback=initialize";
  document.body.appendChild(script);
}

window.onload = loadScript;


// codeAddress('London')
