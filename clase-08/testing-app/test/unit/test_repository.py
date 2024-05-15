import unittest
from unittest.mock import MagicMock
from repositories import userRepository
from models import user

class TestUserRepository(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock()
        self.repository = userRepository.UserRepository(self.mock_db)

    def test_get_all(self):
        mock_session = self.mock_db.session
        mock_query = mock_session.query.return_value
        
        mock_users = [
            user.User(id=1, name="Leandro", email="lean@gmail.com"),
            user.User(id=2, name="Federico", email="fede@gmail.com")
        ]

        mock_query.all.return_value = mock_users

        result = self.repository.get_all()

        mock_session.query.assert_called_once_with(user.User)
        self.assertEqual(result, mock_users)

    def test_create(self):
        self.repository.create('Leo', 'leo@gmail.com')

        self.mock_db.session.add.assert_called_once()
        self.mock_db.session.commit.assert_called_once()

if __name__ == '__main__':
    unittest.main()
