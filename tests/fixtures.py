import pytest
from trace.models.point import Point

@pytest.fixture
def gp_place():
	return {u'rating': 3.9, 
		u'name': u'Koala T Caf\xe9', 
		u'reference': u'CmRSAAAALivgQPOjmexiZSy34IFaqzQn69qF0_KpMe-uSD0DC1FDjIBPimyD7g0O0CTvDetLkCwzhmkqbVSrjZx6IqhP5qB9XmFrwwuEafxauXoE_ZVxQvBsRKJhLRZUu8g_07RDEhC9xzY5Bdg-J2v2v07ftOtKGhTlWYmkZn24QG0HJio8jAc5orULKQ', 
		u'price_level': 1, 
		u'geometry': {u'location': {u'lat': 34.0623974, u'lng': -118.4475638}, u'viewport': {u'northeast': {u'lat': 34.0636840802915, u'lng': -118.4461623197085}, u'southwest': {u'lat': 34.0609861197085, u'lng': -118.4488602802915}}}, 
		u'opening_hours': {u'weekday_text': [], u'open_now': False}, 
		u'place_id': u'ChIJE8wEhYO8woARzV9If3c3Ta4', u'vicinity': u'10965 Weyburn Avenue, Los Angeles', u'photos': [{u'photo_reference': u'test_photo_reference', u'width': 5312, u'html_attributions': [u'<a href="https://maps.google.com/maps/contrib/102856103254091034976/photos">Zhiwen Huang</a>'], u'height': 2988}], u'scope': u'GOOGLE', u'id': u'89fd6508ba52932d08e29f4c05588188118eec28', u'types': [u'cafe', u'restaurant', u'food', u'point_of_interest', u'establishment'], u'icon': u'https://maps.gstatic.com/mapfiles/place_api/icons/restaurant-71.png'}

@pytest.fixture
def sample_cluster_1():
	return [
		Point(**{"id": None,"lat":37.79025862920178,"lng":-122.39991277482,"alt":None,"floor_level":None,"vertical_accuracy":None,"horizontal_accuracy":None,"account_id":None,"created_at":"2016-08-02T01:03:59.998-07:00"}),
		Point(**{"id":None,"lat":37.79028082024202,"lng":-122.3998704144385,"alt":None,"floor_level":None,"vertical_accuracy":None,"horizontal_accuracy":None,"account_id":None,"created_at":"2016-08-02T01:22:35-07:00"}),
	]

@pytest.fixture
def sample_cluster_2():
	return [
		Point(**{"id":None,"lat":-8.064706851735771,"lng":114.24230849381,"alt":2256.371217194963,"floor_level":None,"vertical_accuracy":3,"horizontal_accuracy":5,"account_id":None,"created_at":"2016-08-21T22:31:36.999-07:00"}),
		Point(**{"id":None,"lat":-8.063732916496754,"lng":114.2384006829134,"alt":2225.99807673643,"floor_level":None,"vertical_accuracy":4,"horizontal_accuracy":5,"account_id":None,"created_at":"2016-08-21T22:47:21-07:00"}),
		Point(**{"id":None,"lat":-8.066196902662577,"lng":114.2350418866745,"alt":2104.690364005955,"floor_level":None,"vertical_accuracy":6,"horizontal_accuracy":10,"account_id":None,"created_at":"2016-08-21T23:03:09-07:00"}),
	]