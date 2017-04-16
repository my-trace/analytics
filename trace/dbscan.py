import json
import numpy as np
from sklearn.cluster import DBSCAN

class DBScanner(object):
    MIN_SAMPLES = 2

    @classmethod 
    def get_cluster_labels(cls, locations):
        X = np.array([(c.lat, c.lng) for c in locations])
        db = DBSCAN(eps=0.3, min_samples=cls.MIN_SAMPLES).fit(X)
        core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
        core_samples_mask[db.core_sample_indices_] = True
        labels = db.labels_
        return labels

    @classmethod
    def get_averaged_points(cls, locations, labels):
        # currently only returns lat,lng
        # need to add created_at later
        locations_map = {}
        for location, label in zip(locations, labels):
            if label == -1:
                continue
            if locations_map.get(label) is None:
                locations_map[label] = []
            locations_map[label].append(location)

        averaged_locations = []
        for label, coordinates in locations_map.iteritems():
            average_location = get_average_location(coordinates)
            averaged_locations.append(average_location)
        return averaged_locations    

    @classmethod
    def get_significant_points(cls, locations):
        labels = cls.get_cluster_labels(locations)
        significant_points = cls.get_averaged_points(locations, labels)
        return significant_points

	
def get_average_location(coordinates):
    return sum(c.lat for c in coordinates) / len(coordinates), sum(c.lng for c in coordinates) / len(coordinates)

# def transform_to_vector(coordinates):
#     # converts coordinates into 2D vectors
#     return [(c.get('lat'), c.get('lng')) for c in coordinates]
