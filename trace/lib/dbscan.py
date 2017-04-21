import json
import numpy as np
from sklearn.cluster import DBSCAN
from datetime import datetime

class DBScanner(object):
    MIN_SAMPLES = 100
    EPS = 0.0005

    @classmethod 
    def get_cluster_labels(cls, points):
        # todo: eventually 3d dbscan
        X = np.array([(c.lat, c.lng) for c in points])
        db = DBSCAN(eps=cls.EPS, min_samples=cls.MIN_SAMPLES).fit(X)
        core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
        core_samples_mask[db.core_sample_indices_] = True
        labels = db.labels_
        return labels
