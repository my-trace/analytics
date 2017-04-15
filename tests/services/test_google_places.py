import pytest
import os
from trace.services.google_places import GooglePlacesService

@pytest.fixture
def gp_place():
	return {u'rating': 3.9, 
		u'name': u'Koala T Caf\xe9', 
		u'reference': u'CmRSAAAALivgQPOjmexiZSy34IFaqzQn69qF0_KpMe-uSD0DC1FDjIBPimyD7g0O0CTvDetLkCwzhmkqbVSrjZx6IqhP5qB9XmFrwwuEafxauXoE_ZVxQvBsRKJhLRZUu8g_07RDEhC9xzY5Bdg-J2v2v07ftOtKGhTlWYmkZn24QG0HJio8jAc5orULKQ', 
		u'price_level': 1, 
		u'geometry': {u'location': {u'lat': 34.0623974, u'lng': -118.4475638}, u'viewport': {u'northeast': {u'lat': 34.0636840802915, u'lng': -118.4461623197085}, u'southwest': {u'lat': 34.0609861197085, u'lng': -118.4488602802915}}}, 
		u'opening_hours': {u'weekday_text': [], u'open_now': False}, 
		u'place_id': u'ChIJE8wEhYO8woARzV9If3c3Ta4', u'vicinity': u'10965 Weyburn Avenue, Los Angeles', u'photos': [{u'photo_reference': u'test_photo_reference', u'width': 5312, u'html_attributions': [u'<a href="https://maps.google.com/maps/contrib/102856103254091034976/photos">Zhiwen Huang</a>'], u'height': 2988}], u'scope': u'GOOGLE', u'id': u'89fd6508ba52932d08e29f4c05588188118eec28', u'types': [u'cafe', u'restaurant', u'food', u'point_of_interest', u'establishment'], u'icon': u'https://maps.gstatic.com/mapfiles/place_api/icons/restaurant-71.png'}

def test_to_mt_places_dict(gp_place):
	result = GooglePlacesService.to_mt_places_dict(gp_place)
	expected_result = {
		'name': u'Koala T Caf\xe9',
		'lat': 34.0623974,
		'lng': -118.4475638,
		'photo': 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&key=TEST_GP_API_KEY&photoreference=test_photo_reference',
	}
	assert result == expected_result

# def 