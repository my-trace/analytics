from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref, deferred
from sqlalchemy.ext.declarative import declared_attr
from trace.extensions import db
from trace.services.places import PlacesService

class SignificantPoint(db.Model):
    __tablename__ = 'significant_points'

    id = db.Column(UUID, primary_key=True)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    entered = db.Column(db.DateTime(timezone=True))
    departed = db.Column(db.DateTime(timezone=True))


    # account = relationship('Account')

    def __init__(self, lat, lng, entered, departed, num_points, account_id=None):
        self.lng = lng
        self.lat = lat
        self.account_id = account_id        
        self.entered = entered
        self.departed = departed
        self.num_points = num_points
        self.ranked_places = []
        # self.created_at = datetime.fromtimestamp(created_at / 1000.0) if created_at else datetime.utcnow()
        
    
    def __repr__(self):
        return '<Point lat=(%s) lng=(%s)>' % (self.lat, self.lng)

    def to_dict(self):
        return { c.name: getattr(self, c.name) for c in self.__table__.columns }

    def to_sparse_dict(self):
        # only creates dict from undeferrable columns
        # columns are deferrable to decrease query time
        # 'created_at': self.created_at
        return {'lat': self.lat, 
                'lng': self.lng, 
                # 'entered': self.entered, 
                # 'departed': self.departed, 
                'num_points': self.num_points,
                'ranked_places': self.ranked_places,
                }

    def populate_with_places(self):
        self.ranked_places = PlacesService.get_places_by_significant_point(self)

    @declared_attr
    def account_id(self):
        return db.Column(db.BigInteger, db.ForeignKey('accounts.id'))




