import os, json

from datetime import datetime, timedelta
from flask import Flask, request as req, Response, jsonify, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import (
    IntegrityError
)

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
# this adds a lot of overhead, so we'll disable it
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from helpers import fb_auth, bulk_insert_points
from models import Point, Account

@app.route('/health')
def health():
    return 'healthy'

@app.route('/users', methods=['GET', 'POST'])
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

@app.route('/points', methods=['GET', 'POST'])
def points():
    print 'started request'
    if req.method == 'POST':
        points = json.loads(req.data)
        # TODO: will get account_id from wrapper instead of authorization
        account_id = req.headers['Authorization']
        for point in points:
            point.update({'account_id': account_id})
        bulk_insert_points(db, points)

        return Response('', status=201)

    else:
        lower = datetime.now() - timedelta(weeks=22)
        upper = datetime.now() - timedelta(weeks=21)
        if 'from' in req.args:
            lower = datetime.fromtimestamp(int(req.args.get('from')) / 1000.0)
        if 'until' in req.args:
            upper = datetime.fromtimestamp(int(req.args.get('until')) / 1000.0)
        if upper < lower:
            res = json.dumps({ 'message': 'Upper bound cannot be less than lower bound.' })
            return Response(res, status=400, mimetype='application/json')
        # remove this
        account_id = 'c2e07d98-a6c3-4ac5-a515-4c7145b29f38'
        print os.environ['DEV_DB_URL']
        points = Point.query.filter_by(account_id=account_id) \
            .filter(Point.created_at >= lower) \
            .filter(Point.created_at <= upper) \
            .all()
        print len(points)
        return jsonify([point.to_dict() for point in points])

@app.route('/')
def root():
    return send_from_directory('./../client', 'index.html')

@app.route('/js/<path:path>')
def js(path):
    return send_from_directory('./../client/js', path)

if __name__ == '__main__':
    app.run()
