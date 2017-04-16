import pytest
from trace.dbscan import DBScanner
from tests.fixtures import *

def test_get_significant_points(sample_cluster_1, sample_cluster_2):
	points = sample_cluster_1 + sample_cluster_2
	DBScanner.MIN_SAMPLES = 2
	results = DBScanner.get_significant_points(points)
	cluster_1_average = sum(c.lat for c in sample_cluster_1) / len(sample_cluster_1), sum(c.lng for c in sample_cluster_1) / len(sample_cluster_1)
	cluster_2_average = sum(c.lat for c in sample_cluster_2) / len(sample_cluster_2), sum(c.lng for c in sample_cluster_2) / len(sample_cluster_2)
	print results
	assert results == [cluster_1_average, cluster_2_average]


