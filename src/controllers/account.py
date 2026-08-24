from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from sqlalchemy import inspect

from src.app import db
from src.models.account import Account
from src.utils import requires_role


def _create_account():
    data = request.json
    account = Account(
        user_id=data['user_id'],
        holder=data['holder'],
        balance=data['balance'],
    )
    db.session.add(account)
    db.session.commit()
    db.session.refresh(account)

    return account.to_dict()


def _list_accounts():
    query = db.select(Account)
    accounts = db.session.execute(query).scalars()
    result = [account.to_dict() for account in accounts]

    return result


def _get_account(id):
    account = db.get_or_404(Account, id)
    
    return account.to_dict()


def _update_account(id):
    data = request.json
    account = db.get_or_404(Account, id)
    # print(account)
    mapper = inspect(Account)
    for column in mapper.attrs:
        # print(column.key)
        if column.key in data:
            setattr(account, column.key, data[column.key])
    db.session.commit()
    db.session.refresh(account)

    return account.to_dict()


def _delete_account(id):
    account = db.get_or_404(Account, id)
    db.session.delete(account)
    db.session.commit()


app = Blueprint('account', __name__, url_prefix='/accounts')


@app.route('/', methods=['POST'])
@jwt_required()
@requires_role(['admin', 'normal'])
def create_account():
    return {'account': _create_account()}, HTTPStatus.CREATED


@app.route('/', methods=['GET'])
def list_accounts():
    if request.method == 'GET':
        return {'accounts': _list_accounts()}, HTTPStatus.OK


@app.route('/<int:id>', methods=['GET'])
def get_account(id):
    if request.method == 'GET':
        return _get_account(id), HTTPStatus.OK


@app.route('/<int:id>/update', methods=['PATCH'])
def update_post(id):
    if request.method == 'PATCH':
        return _update_account(id), HTTPStatus.OK


@app.route('/<int:id>/delete', methods=['DELETE'])
def delete_account(id):
    if request.method == 'DELETE':
        _delete_account(id)
        return {"messsage": "Account deleted"}, HTTPStatus.NO_CONTENT
