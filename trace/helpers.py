import requests
import json, functools
import os


from flask import request as req, Response
from sqlalchemy import inspect

# from models import (
#     Point,
# )

# points_column = inspect(Point).columns.keys()

def fb_auth(action):
    @functools.wraps(action)
    def wrap(req):
        if 'Authorization' not in req.headers:
            res = json.dumps({ 'message': 'unauthorized' })
            return Response(res, status=401, mimetype='application/json')
        facebook_token = req.headers['Authorization']
        app_token = os.getenv('APP_TOKEN')
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




