from flask_restx import fields


def get_model_create_response(namespace):
    return namespace.model(
        "GenericCreateResponse",
        {
            "id": fields.Integer(readOnly=True),
            "message": fields.String(required=True),
        },
    )


def get_model_error_response(namespace):
    return namespace.model(
        "GenericCreateResponse",
        {
            "message": fields.String(required=True),
        },
    )
