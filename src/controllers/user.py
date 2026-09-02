from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from src.services.user import UserServices
from src.utils import requires_role

services = UserServices
app = Blueprint('user', __name__, url_prefix='/users')


@app.route('/', methods=['GET', 'POST'])
@jwt_required()
@requires_role(['admin', 'normal'])
def list_or_create_user():
    if request.method == 'POST':
        services._create_user()
        return {'message': 'The user was created!'}, HTTPStatus.CREATED
    else:
        return services._list_users(), HTTPStatus.OK


@app.route('/<int:id>', methods=['GET'])
def get_user(id):
    return services._get_user(id), HTTPStatus.OK


@app.route('/<int:id>', methods=['PATCH'])
@jwt_required()
@requires_role(['admin', 'normal'])
def update_user(id):
    return services._update_user(id), HTTPStatus.OK


@app.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@requires_role(['admin', 'normal'])
def delete_user(id):
    services._delete_user(id)
    return {'message': 'User deleted'}, HTTPStatus.OK
