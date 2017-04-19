import pytest
from trace.lib.dbscan import DBScanner
from tests.fixtures import *

def test_get_cluster_labels(sample_cluster_1, sample_cluster_2):
	points = sample_cluster_1 + sample_cluster_2
	DBScanner.MIN_SAMPLES = 2
	labels = DBScanner.get_cluster_labels(points)
	assert list(labels) == [0, 0, -1, -1, -1]


