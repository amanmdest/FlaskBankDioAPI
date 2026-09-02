from functools import wraps
from http import HTTPStatus

from flask_jwt_extended import get_jwt_identity

from src.app import db
from src.models.user import User


def requires_role(role_name: list):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            user_id = get_jwt_identity()
            user = db.get_or_404(User, user_id)

            if user.role.name not in role_name:
                return {
                    'message': 'Current user does not have access'
                }, HTTPStatus.FORBIDDEN
            return f(*args, **kwargs)

        return wrapped

    return decorator


def squared(x):
    return x**2
