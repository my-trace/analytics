import requests
import os

# GP_API_KEY=os.environ['GP_API_KEY']
GP_API_KEY='test'

GOOGLE_PLACES_SEARCH_URL='https://maps.googleapis.com/maps/api/place/nearbysearch/json?rankby=distance&key={api_key}'.format(api_key=GP_API_KEY)

GOOGLE_PLACES_DETAILS_URL='https://maps.googleapis.com/maps/api/place/details/json?key={api_key}'.format(api_key=GP_API_KEY)

GOOGLE_PLACES_PHOTO_URL='https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&key={api_key}'.format(api_key=GP_API_KEY)

class GooglePlace(object):
    def __init__(self, name, lat, lng, place_id, photo_reference, periods=None):
        self.name = name
        self.lat = lat
        self.lng = lng
        self.place_id = place_id
        self.periods if periods is not None else self.get_hours()
        self.photo = self.get_photo_link(photo_reference)


    @classmethod
    def get_places_from_coordinates(cls, lat, lng):
        url = '{}&location={},{}'.format(GOOGLE_PLACES_SEARCH_URL, lat, lng)
        response = requests.get(url)
        result = response.json()['results']
        return result


    @classmethod
    def get_photo_link(cls, photo_reference):
        url = '{}&photoreference={}'.format(GOOGLE_PLACES_PHOTO_URL, photo_reference)
        return GOOGLE_PLACES_PHOTO_URL.format(photoreference=photo_reference)


    # just use opening hours
    def get_hours(self):
        place_id = self.place_id
        url = '{}&placeid={}'.format(GOOGLE_PLACES_DETAILS_URL,place_id)
        response = requests.get(GOOGLE_PLACES_DETAILS_URL).format(place_id)
        result = response.json()['result']
        periods = result['opening_hours']['periods']
        return periods

    @classmethod
    def to_mt_places_dict(cls, result):
        return {
            'name': str(result['name'].encode('utf-8')),
            # 'periods': result.periods,
            'lat': result['geometry']['location']['lat'],
            'lng': result['geometry']['location']['lng'],
            # 'type': type,
            'photo': cls.get_photo_link(result['photos'][0]['photo_reference']),
        }


