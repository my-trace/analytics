import os, json

from datetime import datetime, timedelta
from flask import Flask, request as req, Response, jsonify, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import (
    IntegrityError
)

from trace.services.places import PlacesService
from trace.extensions import db
import sys
from trace.utils import nocache
from trace.helpers import fb_auth
from trace.lib.dbscan import DBScanner
from trace.models.point import Point
from trace.models.account import Account
from trace.services.points import PointsService 
from trace.services.significant_points_service import SignificantPointsService
from flask_redis import FlaskRedis
import json
redis_store = FlaskRedis()

sys.path.insert(0, '/opt/python/current/app/trace')

application = Flask(__name__)
application.config.from_object(os.environ['APP_SETTINGS'])
# this adds a lot of overhead, so we'll disable it
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

def configure_extensions(app):
    redis_store.init_app(app)
    db.init_app(app)

configure_extensions(application)

@application.route('/users', methods=['GET', 'POST'])
def users():
    if req.method == 'POST':
        data = json.loads(req.data)
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
        return jsonify(items=[account.to_dict() for account in accounts])

@application.route('/points')
def points():
    # default to one week
    now = datetime.now()
    one_week_ago = now - timedelta(days=7)
    print 'fetching points'
    points = redis_store.get('points')
    if not points:
        print 'not in cache'
        points = PointsService.get_points_from_range(one_week_ago, now)
        points = [point.to_sparse_dict() for point in points]
        print points
        redis_store.set('points', json.dumps(points))
    else:
        points = json.loads(points)
    return jsonify(points)

@application.route('/places', methods=['GET'])
def places():
    # default to one week
    now = datetime.now()
    one_week_ago = now - timedelta(days=7)
    significant_places = redis_store.get('places')
    significant_places = None
    if not significant_places:
        print 'fetching places'
        points = PointsService.get_points_from_range(one_week_ago, now)
        print 'converting to signficant points'
        # significant_points = DBScanner.get_significant_points(points)
        
        ## currently just gets the closest place without timestamp
        significant_points = SignificantPointsService.create_significant_points_from_points(points)
        print 'fetching places from significant location', len(significant_points)
        significant_places = [sp.to_sparse_dict() for sp in significant_points]
        # significant_places = PlacesService.get_places_by_significant_points(significant_points)
        redis_store.set('places', json.dumps(significant_places))
        print len(significant_places)
    return jsonify(significant_places)


@application.route('/')
def root():
    return send_from_directory('./../client', 'index.html')

@application.route('/js/<path:path>')
@nocache
def js(path):
    return send_from_directory('./../client/js', path)

@application.route('/data/<path:path>')
def data(path):
    return send_from_directory('./../client/data', path)

@application.route('/health')
@nocache
def health():
    print 'healthy'
    return 'healthy'

if __name__ == '__main__':
    application.run()
