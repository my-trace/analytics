import React from 'react';
import ReactDOM from 'react-dom';
import InspectListView from './components/InspectListView';

ReactDOM.render(
  <InspectListView />,
  document.getElementById('inspectView')
);

var map;
function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: -34.397, lng: 150.644},
    zoom: 8
  });
  console.log('staarting query wow');
  // getPoints().then(renderLine);
  // getPlaces().then(renderMarkers);
}

global.initMap = initMap;

function renderLine(coordinates) {
  console.log(coordinates);
  // let coordinates = coordinates
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

function renderMarkers(places) {
  for (place of places) {
    let latLng = {lat: place.lat, lng: place.lng};
    var marker = new google.maps.Marker({
      position: latLng,
      map: map,
      label: String(place.num_points),
    });
  }
}

function getPlaces() {
  return fetch(`/places`).then(function(response) {
    return response.json()
  }).then(function(body) {
    console.log(body)
    return body
  });
}


function getPoints(accountId, from, until) {
  console.log('starting fetchs')
  return fetch(`/points`).then(function(response) {
    return response.json()
  }).then(function(body) {
    console.log(body)
    return body
  });
}

// function displayList() {
//   let places = marker.places;
//   ReactDOM.render(
//     <RecommendationList places=>,
//     document.getElementById('list')
//   );
// }


// class RecommendationList extends React.Component {
//   render() {

//   }
// }









