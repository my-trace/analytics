from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref, deferred
from sqlalchemy.ext.declarative import declared_attr
from trace.extensions import db

class Point(db.Model):
    __tablename__ = 'points'

    id = db.Column(UUID, primary_key=True)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    alt = deferred(db.Column(db.Float))
    floor_level = deferred(db.Column(db.Integer))
    vertical_accuracy = deferred(db.Column(db.Float))
    horizontal_accuracy = deferred(db.Column(db.Float))
    created_at = db.Column(db.DateTime(timezone=True))

    # account = relationship('Account')

    def __init__(self, id, lng, lat, account_id, **props):
        self.id = id
        self.lat = lng
        self.lng = lat
        self.account_id = account_id
        
        created_at = props.get('timestamp')
        self.created_at = datetime.fromtimestamp(created_at / 1000.0) if created_at else datetime.utcnow()
        
        self.alt = props.get('altitude')
        self.floor_level = props.get('floorLevel')
        self.vertical_accuracy = props.get('verticalAccuracy')
        self.horizontal_accuracy = props.get('horizontalAccuracy')
    
    def __repr__(self):
        return '<Point lat=(%s) lng=(%s)>' % (self.lat, self.lng)

    def to_dict(self):
        return { c.name: getattr(self, c.name) for c in self.__table__.columns if self.c }

    def to_sparse_dict(self):
        # only creates dict from undeferrable columns
        # columns are deferrable to decrease query time
        return {'lat': self.lat, 'lng': self.lng, 'created_at': self.created_at}

    @declared_attr
    def account_id(self):
        return db.Column(db.BigInteger, db.ForeignKey('accounts.id'))




