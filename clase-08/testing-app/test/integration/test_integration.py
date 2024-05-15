import os
import sys
import unittest
import json

current_dir = os.path.abspath(os.path.dirname(__file__))
app_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.insert(0, app_dir)

from app import app

class TestAPIIntegration(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_create_and_get_user(self):
        print('INTEGRATION')
        new_user_data = {'name': 'leandro', 'email': '     leandro@gmail.com    '}
        response_create = self.app.post('/users', json=new_user_data)
        self.assertEqual(response_create.status_code, 200)

        response_get = self.app.get('/users')
        self.assertEqual(response_get.status_code, 200)
        data = json.loads(response_get.data.decode('utf-8'))
        self.assertTrue(any(user['name'] == 'leandro' and user['email'] == 'leandro@gmail.com' for user in data))

        print("INTEGRATION OK")

if __name__ == '__main__':
    unittest.main()