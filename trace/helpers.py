from flask import request as req, Response
from app import app
import requests
import json, functools


def fb_auth(action):
    @functools.wraps(action)
    def wrap():
        if 'Authorization' not in req.headers:
            res = json.dumps({ 'message': 'unauthorized' })
            return Response(res, status=401, mimetype='application/json')
        their_token = req.headers['Authorization']
        our_token = app.config['APP_TOKEN']
        reply = requests.get(
            'https://graph.facebook.com/debug_token?' + 
            'input_token=' + their_token +
            '&access_token=' + our_token)
        reply_body = json.loads(reply.text)
        if reply_body['data']['is_valid']:
            user_id = reply_body['data']['user_id']
            return action(user_id)
        else:
            res = json.dumps({ 'message': reply_body['data'] })
            return Response(res, status=500, mimetype='application/json')

    return wrap
