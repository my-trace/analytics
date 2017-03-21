import json
import numpy as np
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt

json_data = open('./data/sample_locations.json').read()

data = json.loads(json_data)


def transform_to_vector(coordinates):
    # converts coordinates into 2D vectors
    return [(c.get('lat'), c.get('lng')) for c in coordinates]
