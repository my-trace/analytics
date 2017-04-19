from trace.models.significant_point import SignificantPoint
from trace.lib.dbscan import DBScanner
from datetime import datetime, timedelta

class SignificantPointsService(object):
	MIN_DURATION = 30 # number of minutes to be counted as significant


	@classmethod
	def create_significant_points_from_points(cls, points):
		labels = DBScanner.get_cluster_labels(points)
		sp_infos = cls.get_sp_info(points, labels)
		significant_places = []
		for sp_info in sp_infos:
			if sp_info[3] - sp_info[2] < timedelta(minutes=cls.MIN_DURATION):
				continue
			sp = SignificantPoint(
				lat=sp_info[0], lng=sp_info[1], 
				entered=sp_info[2], departed=sp_info[3], 
				num_points=sp_info[4])
			sp.populate_with_places()
			significant_places.append(sp)

		return significant_places


	@classmethod
	def get_sp_info(cls, points, labels):
        # returns lat,lng, first_created_at, last_created_at, num_points
		points_map = {}
		for location, label in zip(points, labels):
		    if label == -1:
		        continue
		    if points_map.get(label) is None:
		        points_map[label] = []
		    points_map[label].append(location)

		sp_infos = []
		for label, coordinates in points_map.iteritems():
		    average_coordinate = get_average_location(coordinates)
		    created_at_bounds = get_created_at_bounds(coordinates)
		    sp_infos.append(average_coordinate + created_at_bounds + (len(coordinates),))
		return sp_infos 

	@classmethod
	def get_points_from_range(cls, start_date, end_date):
		return Point.query.filter(Point.created_at.between(start_date, end_date))

def get_average_location(coordinates):
    '''Return lat,lng'''
    return sum(c.lat for c in coordinates) / len(coordinates), sum(c.lng for c in coordinates) / len(coordinates)

def get_created_at_bounds(coordinates):
	return min(c.created_at for c in coordinates), max(c.created_at for c in coordinates)