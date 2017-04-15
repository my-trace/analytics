from trace.services.google_places import GooglePlace
from trace.utils import 

class PlacesService(object):
    def __init__(self):
        self.name
        self.lat
        self.lng

        self.periods


    @classmethod
    def get_places_by_location(cls, lat, lng):
        return GooglePlace.get_places_by_location(lat, lng)[0]











