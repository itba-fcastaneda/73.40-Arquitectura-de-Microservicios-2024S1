import requests
import unittest

class ContractTestCase(unittest.TestCase):
    def test_get_users_contract(self):
        print("CONTRACT")
        response = requests.get('http://api:5000/users')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        data = response.json()

        self.assertIsInstance(data, list)

        if len(data) > 0:
            print(type(data[0]))
            print(data[0])
            assert data[0].get("email")
            assert data[0].get("name")
            #assert data[0].get("otro")

        print("CONTRACT OK")
if __name__ == '__main__':
    unittest.main()