from http import HTTPStatus

from flask import Blueprint
from flask_jwt_extended import jwt_required

from src.utils import requires_role
from src.services.account import AccountServices



services = AccountServices
app = Blueprint('account', __name__, url_prefix='/accounts')


@app.route('/', methods=['POST'])
@jwt_required()
@requires_role(['admin', 'normal'])
def create_account():
    return {'account': services._create_account()}, HTTPStatus.CREATED


@app.route('/', methods=['GET'])
def list_accounts():
    return {'accounts': services._list_accounts()}, HTTPStatus.OK


@app.route('/<int:id>', methods=['GET'])
def get_account(id):
    return services._get_account(id), HTTPStatus.OK


@jwt_required()
@requires_role(['admin', 'normal'])
@app.route('/<int:id>', methods=['PATCH'])
def update_account(id):
    return services._update_account(id), HTTPStatus.OK


@jwt_required()
@requires_role(['admin', 'normal'])
@app.route('/<int:id>', methods=['DELETE'])
def delete_account(id):
    services._delete_account(id)
    return {'message': 'Account deleted'}, HTTPStatus.OK
