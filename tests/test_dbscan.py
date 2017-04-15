import pytest
from trace.dbscan import DBScanner


@pytest.fixture
def sample_cluster_1():
	return [
		{"id": None,"lat":37.79025862920178,"lng":-122.39991277482,"alt":None,"floor_level":None,"vertical_accuracy":None,"horizontal_accuracy":None,"account_id":None,"created_at":"2016-08-02T01:03:59.998-07:00"},
		{"id":None,"lat":37.79028082024202,"lng":-122.3998704144385,"alt":None,"floor_level":None,"vertical_accuracy":None,"horizontal_accuracy":None,"account_id":None,"created_at":"2016-08-02T01:22:35-07:00"}
	]

@pytest.fixture
def sample_cluster_2():
	return [
		{"id":None,"lat":-8.064706851735771,"lng":114.24230849381,"alt":2256.371217194963,"floor_level":None,"vertical_accuracy":3,"horizontal_accuracy":5,"account_id":None,"created_at":"2016-08-21T22:31:36.999-07:00"},
		{"id":None,"lat":-8.063732916496754,"lng":114.2384006829134,"alt":2225.99807673643,"floor_level":None,"vertical_accuracy":4,"horizontal_accuracy":5,"account_id":None,"created_at":"2016-08-21T22:47:21-07:00"},
		{"id":None,"lat":-8.066196902662577,"lng":114.2350418866745,"alt":2104.690364005955,"floor_level":None,"vertical_accuracy":6,"horizontal_accuracy":10,"account_id":None,"created_at":"2016-08-21T23:03:09-07:00"}
	]


def test_get_significant_points(sample_cluster_1, sample_cluster_2):
	points = sample_cluster_1 + sample_cluster_2
	DBScanner.MIN_SAMPLES = 2
	results = DBScanner.get_significant_points(points)
	cluster_1_average = sum(c['lat'] for c in sample_cluster_1) / len(sample_cluster_1), sum(c['lng'] for c in sample_cluster_1) / len(sample_cluster_1)
	cluster_2_average = sum(c['lat'] for c in sample_cluster_2) / len(sample_cluster_2), sum(c['lng'] for c in sample_cluster_2) / len(sample_cluster_2)
	print results
	assert results == [cluster_1_average, cluster_2_average]


