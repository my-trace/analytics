from geopy.distance import vincenty

def get_distance_between_coordinates(coord1, coord2):
    return vincenty(coord1, coord2).km
