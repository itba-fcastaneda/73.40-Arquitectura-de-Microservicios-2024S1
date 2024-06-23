import pytest
from src.api.models.users import User

TOKEN_TYPES = ["access", "refresh"]


def test_passwords_are_random(test_app, test_database, add_user):
    user_one = add_user("fede", "fede@gmail.com", "test")
    user_two = add_user("fedec", "fedec@gmail.com", "test")
    assert user_one.password != user_two.password


@pytest.mark.parametrize("token_type", TOKEN_TYPES)
def test_encode_token(test_app, test_database, add_user, token_type):
    user = add_user("fede", "fede@gmail.com", "test")
    token = User.encode_token(user.id, token_type)
    assert isinstance(token, str)


@pytest.mark.parametrize("token_type", TOKEN_TYPES)
def test_decode_token(test_app, test_database, add_user, token_type):
    user = add_user("fede", "fede@gmail.com", "test")
    token = User.encode_token(user.id, token_type)
    token_user_id = User.decode_token(token)
    assert isinstance(token_user_id, int)
    assert user.id == token_user_id
