from app import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref
from datetime import datetime


class Account(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(timezone=True)) 

    points = relationship('Point', cascade="delete")

    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return '<Account email=(%s)>' % self.email

    def to_dict(self):
        return { c.name: getattr(self, c.name) for c in self.__table__.columns }


class Point(db.Model):
    __tablename__ = 'points'

    id = db.Column(UUID, primary_key=True)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    alt = db.Column(db.Float)
    floor_level = db.Column(db.Integer)
    vertical_accuracy = db.Column(db.Float)
    horizontal_accuracy = db.Column(db.Float)
    account_id = db.Column(db.BigInteger, db.ForeignKey('accounts.id'))
    created_at = db.Column(db.DateTime(timezone=True))

    account = relationship('Account')

    def __init__(self, id, lat, lng, account_id, **props):
        self.id = id
        self.lat = lat
        self.lng = lng
        self.account_id = account_id
        
        created_at = props.get('created_at')
        self.created_at = datetime.fromtimestamp(created_at / 1000.0) if created_at else datetime.utcnow()
        
        self.alt = props.get('alt')
        self.floor_level = props.get('floor_level')
        self.vertical_accuracy = props.get('vertical_accuracy')
        self.horizontal_accuracy = props.get('horizontal_accuracy')
    
    def __repr__(self):
        return '<Point lat=(%s) lng=(%s)>' % (self.lat, self.lng)

    def to_dict(self):
        return { c.name: getattr(self, c.name) for c in self.__table__.columns }




