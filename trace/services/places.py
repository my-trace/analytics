from trace.services.google_places import GooglePlacesService
# from trace.utils import 

class PlacesService(object):
    def __init__(self):
        self.name
        self.lat
        self.lng
        self.periods


    @classmethod
    def get_places_by_significant_point(cls, lat, lng):
    	# just gets the top ranking location for now
    	results  = GooglePlacesService.get_places_from_coordinates(lat, lng)
        mt_places = [GooglePlacesService.to_mt_places_dict(result) for result in results]
        return mt_places[0]

    @classmethod
    def get_places_by_significant_points(cls, significant_points):
    	# just gets the top ranking location for now
        return [cls.get_places_by_significant_point(p[0], p[1]) for p in significant_points]











