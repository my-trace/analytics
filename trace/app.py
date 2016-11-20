import os, json

from datetime import datetime, timedelta
from flask import Flask, request as req, Response, jsonify
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
@fb_auth
def users(facebook_id):
    if req.method == 'POST':
        existing_account = Account.query.filter_by(id=account_id).first()
        if existing_account:
            res = jsonify({ 'message': 'already registered' })
            res.status_code = 400
            return res
        data = json.loads(req.data)
        new_account = Account(facebook_id=facebook_id, name=data['name'], email=data['email'])
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
    if req.method == 'POST':
        points = json.loads(req.data)
        # TODO: will get account_id from wrapper instead of authorization
        account_id = req.headers['Authorization']
        for point in points:
            point.update({'account_id': account_id})
        bulk_insert_points(db, points)

        return Response('', status=201)

    else:
        lower = datetime.now() - timedelta(weeks=1)
        upper = datetime.now()
        if 'from' in req.args:
            lower = datetime.fromtimestamp(int(req.args.get('from')) / 1000.0)
        if 'until' in req.args:
            upper = datetime.fromtimestamp(int(req.args.get('until')) / 1000.0)
        if upper < lower:
            res = json.dumps({ 'message': 'Upper bound cannot be less than lower bound.' })
            return Response(res, status=400, mimetype='application/json')
        points = Point.query.filter_by(account_id=account_id) \
            .filter(Point.created_at >= lower) \
            .filter(Point.created_at <= upper) \
            .all()
        return jsonify([point.to_dict() for point in points])



if __name__ == '__main__':
    app.run()
