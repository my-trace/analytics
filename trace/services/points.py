from trace.models.point import Point

class PointsService(object):
    @classmethod
    def get_points_from_range(cls, start_date, end_date):
        return Point.query.filter(Point.created_at.between(start_date, end_date))