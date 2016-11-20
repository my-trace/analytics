import requests
import json, functools

from app import app
from flask import request as req, Response
from sqlalchemy import inspect

from models import (
    PointTemp,
    Point,
)

points_column = inspect(Point).columns.keys()

def fb_auth(action):
    @functools.wraps(action)
    def wrap(req):
        if 'Authorization' not in req.headers:
            res = json.dumps({ 'message': 'unauthorized' })
            return Response(res, status=401, mimetype='application/json')
        facebook_token = req.headers['Authorization']
        app_token = app.config['APP_TOKEN']
        reply = requests.get(
            'https://graph.facebook.com/debug_token?' + 
            'input_token=' + facebook_token +
            '&access_token=' + app_token)
        reply_body = json.loads(reply.text)
        if reply_body['data']['is_valid']:
            user_id = reply_body['data']['user_id']
            return action(user_id)
        else:
            res = json.dumps({ 'message': reply_body['data'] })
            return Response(res, status=500, mimetype='application/json')

    return wrap

def bulk_insert_points(db, points):
    if not points:
        return
    engine = db.engine
    sql = """
    BEGIN;
    LOCK TABLE points_temp IN EXCLUSIVE MODE;
    TRUNCATE points_temp;
    COMMIT;
    """
    engine.execute(sql)
    point_temps = [PointTemp(**point) for point in points]
    db.session.bulk_save_objects(point_temps)
    db.session.commit()
    sql = """
    BEGIN;
    LOCK TABLE points IN EXCLUSIVE MODE;
    INSERT INTO points ({columns}) SELECT {columns} from points_temp WHERE NOT EXISTS (SELECT 1 FROM points WHERE points_temp.id = points.id);
    COMMIT;
    """.format(columns=','.join(points_column))
    engine.execute(sql)




