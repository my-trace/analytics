import requests


GP_API_KEY=os.environ['GP_API_KEY']

GOOGLE_PLACES_SEARCH_URL='https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&rankby=distance&key={api_key}}'.format(api_key=GP_API_KEY)

GOOGLE_PLACES_DETAILS_URL='https://maps.googleapis.com/maps/api/place/details/json?placeid={place_id}&key={api_key}'.format(GP_API_KEY)

class GooglePlace(object):
    def __init__(self, name, lat, lng, place_id, periods=None)
        self.name = name
        self.lat = lat
        self.lng = lng
        self.place_id = place_id
        self.periods if periods is not None else self.get_hours()


    @classmethod
    def get_places_from_coordinates(cls, lat, lng):
        response = requests.get(GOOGLE_PLACES_SEARCH_URL.format(lat, lng))
        result = response.json()['results']




    # just use opening hours
    def get_hours(self):
        place_id = self.place_id
        response = requests.get(GOOGLE_PLACES_DETAILS_URL).format(place_id)
        result = response.json()['result']
        periods = result['opening_hours']['periods']
        return periods


    def to_mt_places_dict(self):
        return {
            'name': self.name,
            'periods': self.periods,
            'lat': self.lat,
            'lng': self.lng,
            # 'type': type,
            # 'photo':
        }



