from http import HTTPStatus

from flask import Blueprint

from src.services.transfer import TransferServices

services = TransferServices
app = Blueprint('transfer', __name__, url_prefix='/transfers')


@app.route('/<int:account_id>', methods=['POST'])
def make_transfer(account_id):
    return {
        'transfer': services._make_transfer(account_id)
    }, HTTPStatus.CREATED


@app.route('/', methods=['GET'])
def list_transfers():
    return {'transfers': services._list_transfers()}, HTTPStatus.OK


@app.route('/<int:account_id>', methods=['GET'])
def list_transfers_by_account(account_id):
    return {
        'transfers': services._list_transfers_by_account(account_id)
    }, HTTPStatus.OK


@app.route('/<int:id>', methods=['GET'])
def get_transfer(id):
    return {'transfer': services._get_transfer(id)}, HTTPStatus.OK
