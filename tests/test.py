import unittest
import json
from trace.app import app, db
from trace.models import Account, Point

Point.query.delete()
Account.query.delete()
db.session.commit()

headers = { 'Authorization': app.config.get('ANDY_TOKEN') }
account_id = None

class flaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test0_health(self):
        res = self.app.get('/health')
        assert res.status == '200 OK'
        assert res.mimetype == 'text/html'
        assert res.data == 'healthy'

    def test1_users_post(self):
        res = self.app.get('/users', headers=headers)
        assert res.status == '200 OK'
        assert res.mimetype == 'application/json'
        data = json.loads(res.data)
        assert len(data) == 0
        
        data = {
            'name': 'Andy Carlson',
            'email': 'acarl005@g.ucla.edu' }
        res = self.app.post('/users', 
            headers=headers,
            content_type='application/json',
            data=json.dumps(data))
        res_data = json.loads(res.data)
        assert res.status == '201 CREATED'
        assert res_data['name'] == data['name']
        assert res_data['email'] == data['email']
        global account_id
        account_id = res_data['id']

    def test2_users_get(self):
        res = self.app.get('/users', headers=headers)
        assert res.status == '200 OK'
        assert res.mimetype == 'application/json'
        data = json.loads(res.data)
        assert len(data) == 1

    def test3_users_no_auth(self):
        data = {
            'name': 'Andy Carlson',
            'email': 'acarl005@g.ucla.edu' }
        res = self.app.post('/users', 
            content_type='application/json',
            data=json.dumps(data))
        assert res.status == '401 UNAUTHORIZED'

    def test4_point_post(self):
        res = self.app.get('/points', headers=headers)
        assert res.status == '200 OK'
        assert res.mimetype == 'application/json'
        data = json.loads(res.data)
        assert len(data) == 0

        data = [
            {
                "lat": 120.02352,
                "lng": 33.3523,
                "id": "b3836d32-70da-11e6-8895-37d9897f529d",
                "created_at": 1472798220883,
                "alt": 2353.0,
                "vertical_accuracy": 3432 },
            {
                "lat": 120.02353,
                "lng": 33.3521,
                "id": "b8878c46-70da-11e6-a04c-039f23535545",
                "created_at": 1472798220883,
                "floor_level": 3,
                "horizontal_accuracy": 34234.0 },
            {
                "lat": 120.02352,
                "lng": 33.3523,
                "id": "f95bbca4-714f-11e6-a7ee-a32031d1391f",
                "created_at": 1472798220883 },
            {
                "lat": 120.02353,
                "lng": 33.3521,
                "id": "f3317738-714f-11e6-a5ac-3bfbc8b3014d" } ]

        res = self.app.post('/points',
            headers=headers,
            content_type='application/json',
            data=json.dumps(data))

        assert res.status == '201 CREATED'

    def test5_point_get(self):
        res = self.app.get('/points?from=1472703040136', headers=headers)
        assert res.status == '200 OK'
        assert res.mimetype == 'application/json'
        data = json.loads(res.data)
        assert len(data) == 4

        res = self.app.get('/points?from=1472703040136&until=1472803050236', headers=headers)
        assert res.status == '200 OK'
        assert res.mimetype == 'application/json'
        data = json.loads(res.data)
        assert len(data) == 3

    def test6_point_no_auth(self):
        data = [
            {
                "lat": 120.02352,
                "lng": 33.3523,
                "id": "de3d2f00-7165-11e6-8c66-5bc358099a35",
                "created_at": 1472798220883,
                "alt": 2353.0,
                "vertical_accuracy": 3432 } ]
        res = self.app.post('/points',
            content_type='application/json',
            data=json.dumps(data))

        assert res.status == '401 UNAUTHORIZED'

        res = self.app.get('/points')
        assert res.status == '401 UNAUTHORIZED'

    def test7_point_invalid_range(self):
        res = self.app.get('/points?from=1472903940136&until=1472803050236', headers=headers)
        assert res.status == '400 BAD REQUEST'
        data = json.loads(res.data)
        assert data['message'] == 'Upper bound cannot be less than lower bound.'




if __name__ == '__main__':
    unittest.main()
