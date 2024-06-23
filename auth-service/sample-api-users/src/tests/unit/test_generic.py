from src.api.models.generic import (get_model_create_response,
                                    get_model_error_response)


def test_model_create_response(test_namespace):
    model = get_model_create_response(test_namespace)
    assert model.get("id")
    assert model.get("message")


def test_get_model_error_response(test_namespace):
    model = get_model_error_response(test_namespace)
    assert "message" in model
