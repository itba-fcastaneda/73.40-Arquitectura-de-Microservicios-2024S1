import unittest
from unittest.mock import MagicMock
from controllers import userController
from services import userService
from models import user
from flask import Flask, jsonify

class TestUserController(unittest.TestCase):
    def setUp(self):
        self.mock_user_service = MagicMock(spec=userService.UserService)
        self.controller = userController.UserController(self.mock_user_service)

    def test_get_users(self):
        self.mock_user_service.get_users.return_value = [
            user.User(id=1, name="Leandro", email="lean@gmail.com"),
            user.User(id=2, name="Federico", email="fede@gmail.com")
        ]
        app = Flask(__name__)
        
        with app.test_request_context():
            response = self.controller.get_users()

            self.assertEqual(response.status_code, 200)
            data = response.json
            self.assertEqual(len(data), 2)
            self.assertEqual(data[0]['name'], 'Leandro')
            self.assertEqual(data[0]['email'], 'lean@gmail.com')
            self.assertEqual(data[1]['name'], 'Federico')
            self.assertEqual(data[1]['email'], 'fede@gmail.com')

    def test_create_user(self):
        app = Flask(__name__)
        
        with app.test_request_context():
            with unittest.mock.patch('flask.request.get_json') as mock_get_json:
                mock_get_json.return_value = {'name': 'new_user', 'email': 'new_user@example.com'}
                response = self.controller.create_user()
                self.mock_user_service.create_user.assert_called_once_with('new_user', 'new_user@example.com')
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json, {'mensaje': 'Usuario creado exitosamente'})

if __name__ == '__main__':
    unittest.main()


#python3 -m unittest discover test/unit/
#FLASK_ENV=testing python3 -m unittest discover test/integration/

#python3 -m coverage run test/unit/test_repository.py
#python3 -m coverage run -m unittest discover test/unit/
#python3 -m coverage report