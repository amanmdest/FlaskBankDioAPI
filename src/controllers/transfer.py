from http import HTTPStatus

from flask import Blueprint
from flask_jwt_extended import jwt_required

from src.services.transfer import TransferServices
from src.utils import requires_role

services = TransferServices
app = Blueprint('transfer', __name__, url_prefix='/transfers')


@app.route('/<int:account_id>', methods=['POST'])
@jwt_required()
@requires_role(['admin', 'normal'])
def make_transfer(account_id):
    return {
        'transfer': services._make_transfer(account_id)
    }, HTTPStatus.CREATED


@app.route('/', methods=['GET'])
def list_transfers():
    return {'transfers': services._list_transfers()}, HTTPStatus.OK


@app.route('/account/<int:account_id>', methods=['GET'])
def list_transfers_by_account(account_id):
    return {
        'transfers': services._list_transfers_by_account(account_id)
    }, HTTPStatus.OK


@app.route('/<int:id>', methods=['GET'])
def get_transfer(id):
    return services._get_transfer(id), HTTPStatus.OK
