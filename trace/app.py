import os, json

from datetime import datetime, timedelta
from flask import Flask, request as req, Response, jsonify, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import (
    IntegrityError
)

import sys
sys.path.insert(0, '/opt/python/current/app/trace')

application = Flask(__name__)
application.config.from_object(os.environ['APP_SETTINGS'])
# this adds a lot of overhead, so we'll disable it
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(application)



from helpers import fb_auth
# from models import Point, Account

# from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref, deferred
from sqlalchemy.ext.declarative import declared_attr

## will move to another file later
class Account(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow) 
    facebook_id = db.Column(db.BigInteger)

    points = relationship('Point', cascade="delete")

    def __init__(self, facebook_id, name, email):
        self.name = name
        self.email = email
        self.facebook_id = facebook_id

    def __repr__(self):
        return '<Account email=(%s)>' % self.email

    def to_dict(self):
        return { c.name: getattr(self, c.name) for c in self.__table__.columns }

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

    def __init__(self, uuid, longitude, latitude, account_id, **props):
        self.id = uuid
        self.lat = longitude
        self.lng = latitude
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




@application.route('/health')
def health():
    return 'healthy'

@application.route('/users', methods=['GET', 'POST'])
def users():
    if req.method == 'POST':
        data = json.loads(req.data)
        print data
        existing_account = Account.query.filter_by(facebook_id=str(data['id'])).first()
        print 'existing account', existing_account
        if existing_account:
            res = jsonify({ 'message': 'already registered' })
            res.status_code = 201
            return res
        new_account = Account(facebook_id=data['id'], name=data['name'], email=data['email'])
        db.session.add(new_account)
        db.session.commit()
        res = jsonify(new_account.to_dict())
        res.status_code = 201
        return res
    else:
        accounts = Account.query.all()
        return jsonify([account.to_dict() for account in accounts])

@application.route('/points', methods=['GET', 'POST'])
def points():
    print 'hello'
    # lower = datetime.now() - timedelta(weeks=20)
    # upper = datetime.now() - timedelta(weeks=18)
    # if 'from' in req.args:
    #     lower = datetime.fromtimestamp(int(req.args.get('from')) / 1000.0)
    # if 'until' in req.args:
    #     upper = datetime.fromtimestamp(int(req.args.get('until')) / 1000.0)
    # if upper < lower:
    #     res = json.dumps({ 'message': 'Upper bound cannot be less than lower bound.' })
    #     return Response(res, status=400, mimetype='application/json')

    # points = Point.query.filter_by(account_id=account_id) \
    #     .filter(Point.created_at >= lower) \
    #     .filter(Point.created_at <= upper) \
    #     .all()
    # return jsonify([point.to_sparse_dict() for point in points])

@application.route('/')
def root():
    return send_from_directory('./../client', 'index.html')

@application.route('/js/<path:path>')
def js(path):
    return send_from_directory('./../client/js', path)

@application.route('/data/<path:path>')
def data(path):
    return send_from_directory('./../client/data', path)

if __name__ == '__main__':
    application.run()
