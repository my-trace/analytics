import pytest
import os
from trace.services.google_places import GooglePlacesService
from tests.fixtures import *	


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