from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref, deferred
from sqlalchemy.ext.declarative import declared_attr
from trace.extensions import db

class Account(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow) 
    facebook_id = db.Column(db.BigInteger)

    # points = relationship('Point', cascade="delete")

    def __init__(self, facebook_id, name, email):
        self.name = name
        self.email = email
        self.facebook_id = facebook_id

    def __repr__(self):
        return '<Account email=(%s)>' % self.email

    def to_dict(self):
        return { c.name: getattr(self, c.name) for c in self.__table__.columns }