import unittest
import api
import json
from decorators import TOKEN_HEADER_NAME


class RoutesTestCase(unittest.TestCase):

    def setUp(self):
        print("==> Setting up the env for tests!")
        api.app.config['TESTING'] = True
        self.app = api.app.test_client()

    def tearDown(self):
        print("==> Tearing down after tests!")

    def test_index(self):
        resp = self.app.get('/')
        assert "200 OK" == resp.status

    def test_getbyid_OK(self):
        print("\nRunning: test_get_by_id OK")
        resp = self.app.get('/api/getbyid/1')
        assert "200 OK" == resp.status
        assert {"getbyid": "OK"} == json.loads(resp.data)

    def test_getbyid_NOK(self):
        print("\nRunning: test_get_by_id NOOK")
        resp = self.app.get('/api/getbyid/a')
        assert "404 NOT FOUND" == resp.status

    def test_get_OK(self):
        print("\nRunning: test_get OK")
        resp = self.app.get('/api/get')
        assert "200 OK" == resp.status
        assert {"get": "OK"} == json.loads(resp.data)

    def test_post_OK(self):
        print("\nRunning: test_create OK")
        resp = self.app.post('/api/post', data=dict(
            input="input",
        ))
        assert "200 OK" == resp.status
        assert {"post": "OK"} == json.loads(resp.data)

    def test_post_NOOK(self):
        print("\nRunning: test_create NOOK")
        resp = self.app.post('/api/post', data=dict(
            invalid="invalid",
        ))
        assert "400 BAD REQUEST" == resp.status

    def test_put_OK(self):
        print("\nRunning: test_update OK")
        resp = self.app.put('/api/put/1', data=dict(
            put="put",
        ))
        assert "200 OK" == resp.status
        assert {"put": "OK"} == json.loads(resp.data)

    def test_put_NOOK(self):
        print("\nRunning: test_update NOOK")
        resp = self.app.put('/api/put/1', data=dict(
            invalid="invalid",
        ))
        assert "400 BAD REQUEST" == resp.status

    def test_put_not_found_NOOK(self):
        print("\nRunning: test_update NOOK")
        resp = self.app.put('/api/put/4', data=dict(
            put="put",
        ))
        assert "404 NOT FOUND" == resp.status

    def test_delete_OK(self):
        print("\nRunning: test_delete OK")
        resp = self.app.delete('/api/delete/1')
        assert "200 OK" == resp.status
        assert {"delete": "OK"} == json.loads(resp.data)

    def test_delete_NOOK(self):
        print("\nRunning: test_delete NOOK")
        resp = self.app.delete('/api/delete/3')
        assert "404 NOT FOUND" == resp.status

    def test_auth_OK(self):
        print("\nRunning: test_auth OK")
        # user: admin, pass: admin
        resp = self.app.get('/api/auth', headers={
            "Authorization": "Basic YWRtaW46YWRtaW4="})
        assert 200 == resp.status_code
        assert {"auth": "OK"} == json.loads(resp.data)

    def test_auth_NOOK(self):
        print("\nRunning: test_auth NOOK")
        resp = self.app.get('/api/auth',
                            headers={"Authorization": "Basic Test"})
        assert 401 == resp.status_code

    def test_get_token_OK(self):
        print("\nRunning: test_auth_token OK")
        # user: admin, pass: admin
        resp = self.app.get('/api/auth', headers={
            "Authorization": "Basic YWRtaW46YWRtaW4="})
        resp_auth = self.app.get('/api/getwithauth', headers={
            TOKEN_HEADER_NAME: resp.headers[TOKEN_HEADER_NAME]})

        assert 200 == resp_auth.status_code
        assert {"get": "OK"} == json.loads(resp_auth.data)

    def test_get_token_NOOK(self):
        print("\nRunning: test_auth_token NOOK")
        # user: admin, pass: admin
        resp = self.app.get('/api/auth', headers={
            "Authorization": "Basic YWRtaW46YWRtaW4="})

        resp_auth = self.app.get('/api/getwithauth', headers={
            TOKEN_HEADER_NAME: "AnyValueForTokenYWRtaW46YWRtaW4"})

        assert 401 == resp_auth.status_code

    def test_error_handling_OK(self):
        print("\nRunning: test_error_handling OK")
        # user: admin, pass: admin
        resp = self.app.get('/api/error/1')

        assert 500 == resp.status_code
        assert "Error" in json.loads(resp.data)


if __name__ == '__main__':
    unittest.main()
