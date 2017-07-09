import unittest
import requests
import json

class TestUserStats(unittest.TestCase):
    def test_stats(self):
        payload = {'id':'Joao'}
        response = requests.post('http://130.211.125.185/users', data=json.dumps(payload))
        self.assertEqual(response.json(), payload)
        self.assertEqual(response.status_code, 201)
        response = requests.post('http://130.211.125.185/users', data=json.dumps(payload))
        self.assertEqual(response.status_code, 409)

        response = requests.get('http://130.211.125.185/users/Joao/stats')
        self.assertEqual(response.json(), {
            "id": "Joao",
            "hits": 0,
            "topUrls": [],
            "urlCount": 0
            }
        )
        self.assertEqual(response.status_code, 200)

        #Delete user
        response = requests.delete('http://130.211.125.185/user/Joao')
        self.assertEqual(response.status_code, 200)

class TestAddAndDeleteUser(unittest.TestCase):
    def test_add_user(self):
        payload = {'id':'Andre'}
        response = requests.post('http://130.211.125.185/users', data=json.dumps(payload))
        self.assertEqual(response.json(), payload)
        self.assertEqual(response.status_code, 201)

        #Testing conflict
        response = requests.post('http://130.211.125.185/users', data=json.dumps(payload))
        self.assertEqual(response.status_code, 409)

        #Delete user
        response = requests.delete('http://130.211.125.185/user/Andre')
        self.assertEqual(response.status_code, 200)

        #Trying to delete a user that doesnt exists
        response = requests.delete('http://130.211.125.185/user/Andre')
        self.assertEqual(response.status_code, 404)

class TestRedirectionAndStats(unittest.TestCase):
    def test_redirection(self):
        #add user
        payload = {'id':'Bruno'}
        response = requests.post('http://130.211.125.185/users', data=json.dumps(payload))
        self.assertEqual(response.json(), payload)
        self.assertEqual(response.status_code, 201)

        #add url
        payload = {'url':'www.google.com'}
        response = requests.post('http://130.211.125.185/users/Bruno/urls', data=json.dumps(payload))
        resp_json = response.json()
        url_id = resp_json['id']

        #Cant test for id and shortened url because I cant be sure of their value
        self.assertEqual(resp_json['hits'] , 0)
        self.assertEqual(resp_json['url'] , 'http://www.google.com')
        self.assertEqual(response.status_code, 201)

        #redirection
        url = 'http://130.211.125.185/urls/{0}'.format(url_id)
        response = requests.get(url, allow_redirects=False)
        self.assertTrue(response.is_redirect)

        #URL stats
        url = 'http://130.211.125.185/stats/{0}'.format(url_id)
        response = requests.get(url)
        resp_json = response.json()
        self.assertEqual(resp_json['id'] , url_id)
        self.assertEqual(resp_json['hits'] , 1)
        self.assertEqual(resp_json['url'] , 'http://www.google.com')

        #Delete user
        response = requests.delete('http://130.211.125.185/user/Bruno')
        self.assertEqual(response.status_code, 200)

class TestAddAndDeleteURL(unittest.TestCase):
    def test_delete_url(self):
        #add user
        payload = {'id':'Ze'}
        response = requests.post('http://130.211.125.185/users', data=json.dumps(payload))
        self.assertEqual(response.json(), payload)
        self.assertEqual(response.status_code, 201)

        #add url
        payload = {'url':'www.terra.com.br'}
        response = requests.post('http://130.211.125.185/users/Ze/urls', data=json.dumps(payload))
        resp_json = response.json()
        url_id = resp_json['id']

        url = 'http://130.211.125.185/urls/{0}'.format(url_id)
        response = requests.delete(url)
        self.assertEqual(response.status_code, 200)

        #Trying to delete a URL that doesnt exists
        response = requests.delete('http://130.211.125.185/urls/{0}'.format(url_id))
        self.assertEqual(response.status_code, 404)

        #Delete user
        response = requests.delete('http://130.211.125.185/user/Ze')
        self.assertEqual(response.status_code, 200)

class TestCoffee(unittest.TestCase):
    def test_coffee(self):
        response = requests.get('http://130.211.125.185/coffee')
        self.assertEqual(response.status_code, 418)

if __name__ == "__main__":
    unittest.main()
