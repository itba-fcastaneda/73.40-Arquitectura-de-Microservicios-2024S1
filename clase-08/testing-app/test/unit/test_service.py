import unittest
from unittest.mock import MagicMock
from services import userService
from repositories import userRepository
from models import user 

class TestUserService(unittest.TestCase):
    def setUp(self):
        self.mock_repository = MagicMock(spec=userRepository.UserRepository)
        self.user_service = userService.UserService(self.mock_repository)

    def test_get_users(self):
        mock_users = [
            user.User(id=1, name="Leandro", email="lean@gmail.com"),
            user.User(id=2, name="Federico", email="fede@gmail.com")
        ]
        self.mock_repository.get_all.return_value = mock_users
        
        result = self.user_service.get_users()
        
        self.assertEqual(result, mock_users)

    def test_create_user(self):
        self.user_service.create_user("Leo", "   leo@gmail.com    ")
        
        self.mock_repository.create.assert_called_once_with("Leo", "leo@gmail.com") 

if __name__ == '__main__':
    unittest.main()