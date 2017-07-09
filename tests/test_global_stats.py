import unittest
import requests
import json

class TestGlobalStats(unittest.TestCase):
    def test_global_stats(self):
        try:
            payload = {'id':'Romeu'}
            response = requests.post('http://130.211.125.185/users', data=json.dumps(payload))
            self.assertEqual(response.json(), payload)
            self.assertEqual(response.status_code, 201)

            url = 'http://130.211.125.185/stats'
            response = requests.get(url)
            resp_json = response.json()
            first_url_count = resp_json['urlCount']

            #add url
            payloads = [{'url':'github.com'}, {'url':'www.uol.com.br'}, {'url':'stackoverflow.com'}]
            url_ids = []
            for payload in payloads:
                response = requests.post('http://130.211.125.185/users/Romeu/urls', data=json.dumps(payload))
                resp_json = response.json()
                url_id = resp_json['id']
                url_ids.append(url_id)

            #redirection
            cont = 0
            while cont < 2:
                url = 'http://130.211.125.185/urls/{0}'.format(url_ids[0])
                response = requests.get(url, allow_redirects=False)
                self.assertTrue(response.is_redirect)
                cont += 1

            #redirection
            cont = 0
            while cont < 3:
                url = 'http://130.211.125.185/urls/{0}'.format(url_ids[2])
                response = requests.get(url, allow_redirects=False)
                self.assertTrue(response.is_redirect)
                cont += 1

            url = 'http://130.211.125.185/stats'
            response = requests.get(url)
            resp_json = response.json()
            top_urls = resp_json['topUrls']
            url_count = resp_json['urlCount']

            self.assertEqual(top_urls[0]['id'], url_ids[2])
            self.assertEqual(top_urls[1]['id'], url_ids[0])
            self.assertEqual(top_urls[2]['id'], url_ids[1])
            self.assertEqual(url_count, first_url_count+3)

            #Delete URL
            response = requests.delete('http://130.211.125.185/urls/{0}'.format(url_ids[0]))
            self.assertEqual(response.status_code, 200)

            url = 'http://130.211.125.185/stats'.format(url_id)
            response = requests.get(url)
            resp_json = response.json()
            new_url_count = resp_json['urlCount']

            self.assertEqual(new_url_count, url_count-1)

            #Delete user
            response = requests.delete('http://130.211.125.185/user/Romeu')
            self.assertEqual(response.status_code, 200)

        except Exception as err:
            #Delete user
            response = requests.delete('http://130.211.125.185/user/Romeu')
            self.assertEqual(response.status_code, 200)
            raise Exception

if __name__ == "__main__":
    unittest.main()
