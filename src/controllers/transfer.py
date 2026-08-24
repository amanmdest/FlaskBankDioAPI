from http import HTTPStatus

from flask import Blueprint, request

from src.app import db
from src.models.transfer import Transfer


def _create_transfer():
    data = request.json
    transfer = Transfer(
        account_id=data['account_id'],
        amount=data['amount']
        )
    db.session.add(transfer)
    db.session.commit()


def _list_transfer():
    query = db.select(Transfer)
    transfer = db.session.execute(query).scalars()
    result = [transfer.to_dict() for transfer in transfer]
    return result


def _get_transfer(id):
    transfer = db.get_or_404(Transfer, id)
    return {'id': transfer.id, 'transfer': transfer.transfer}


app = Blueprint('transfer', __name__, url_prefix='/transfers')


@app.route('/', methods=['GET', 'POST'])
def list_or_create_transfer():
    if request.method == 'POST':
        _create_transfer()
        return {'message': 'The transfer was created!'}, HTTPStatus.CREATED
    else:
        return {'transfer': _list_transfer()}, HTTPStatus.OK


@app.route('/<int:id>', methods=['GET'])
def get_transfer(id):
    if request.method == 'GET':
        return {'transfer': _get_transfer(id)}, HTTPStatus.OK
