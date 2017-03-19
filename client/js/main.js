var map;
function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: -34.397, lng: 150.644},
    zoom: 8
  });
  console.log('staarting query');
  // console.log(sample_locations.length);
  getPoints().then(renderLine);
}

function renderLine(coordinates) {
  console.log(coordinates);
  var path = new google.maps.Polyline({
    path: coordinates,
    geodesic: true,
    strokeColor: '#FF0000',
    strokeOpacity: 1.0,
    strokeWeight: 2
  });

  path.setMap(map);

  var latlngbounds = new google.maps.LatLngBounds();
  for (var i = 0; i < coordinates.length; i++) {
    latlngbounds.extend(coordinates[i]);
  }
  map.fitBounds(latlngbounds);
}


function getPoints(accountId, from, until) {
  return fetch(`/points`).then(function(response) {
    return response.json()
  }).then(function(body) {
    return body
  });
}







