from trace.services.google_places import GooglePlacesService
# from trace.utils import 

# might need significant point entity later
class PlacesService(object):
    def __init__(self, lat, lng, periods=None):
        # self.name = name
        self.lat = lat
        self.lng = lng
        self.periods = periods


    @classmethod
    def get_places_by_significant_point(self, sp):
    	results  = GooglePlacesService.get_places_from_coordinates(sp.lat, sp.lng)
        mt_places = [GooglePlacesService.to_mt_places_dict(result) for result in results]
        return mt_places

    # def to_dict(self):
    #     return {
    #         'lat': self.lat,
    #         'lng': self.lng,
    #         'num_points': self.num_points,
    #         # 'ranked_places': self.ranked_places
    #     }

    # @classmethod
    # def get_places_by_significant_points(cls, significant_points):
    # 	# just gets the top ranking location for now
    #     places = [PlacesService(lat=sp[0], lng=sp[1], num_points=sp[2]).to_dict() for sp in significant_points]
    #     # places = [cls.get_places_by_significant_point(sp) for sp in significant_points]
    #     return places











