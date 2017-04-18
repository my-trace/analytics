import os, json

from datetime import datetime, timedelta
from flask import Flask, request as req, Response, jsonify, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import (
    IntegrityError
)

from dbscan import DBScanner
from services.places import PlacesService
from extensions import db
import sys
sys.path.insert(0, '/opt/python/current/app/trace')

application = Flask(__name__)
application.config.from_object(os.environ['APP_SETTINGS'])
# this adds a lot of overhead, so we'll disable it
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from helpers import fb_auth
from trace.models.point import Point
from trace.models.account import Account
from trace.services.points import PointsService 

def configure_extensions(app):
    db.init_app(app)

configure_extensions(application)

@application.route('/health')
def health():
    print application.config
    return 'healthy'

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
        return jsonify([account.to_dict() for account in accounts])

@application.route('/places', methods=['GET'])
def places():
    # default to one week
    now = datetime.now()
    one_week_ago = now - timedelta(days=7)
    print 'fetching places'
    locations = PointsService.get_points_from_range(one_week_ago, now)
    print 'converting to signficant points'
    significant_points = DBScanner.get_significant_points(locations)
    print 'fetching places from significant location'
    ## currently just gets the closest place without timestamp
    significant_places = PlacesService.get_places_by_significant_points(significant_points)
    return jsonify(significant_places)

@application.route('/points', methods=['GET'])
def points():
    # default to one week
    now = datetime.now()
    one_week_ago = now - timedelta(days=7)
    print 'fetching points'
    locations = PointsService.get_points_from_range(one_week_ago, now)
    print locations
    return jsonify(locations)


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
