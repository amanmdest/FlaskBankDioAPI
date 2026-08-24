from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from sqlalchemy import inspect

from src.app import db
from src.models.user import User
from src.utils import requires_role


def _create_user():
    data = request.json
    user = User(
        username=data['username'],
        password=data['password'],
        role_id=data['role_id'],
    )
    db.session.add(user)
    db.session.commit()
    db.session.refresh(user)


def _list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars()
    result = [user.to_dict() for user in users]
    return result


def _get_user(id):
    user = db.get_or_404(User, id)
    return user.to_dict()


def _update_user(id):
    data = request.json
    user = db.get_or_404(User, id)
    # print(user)
    mapper = inspect(User)
    # for column in mapper.attrs:
    for column in mapper.columns:
        # print(column.key)
        if column.key in data:
            setattr(user, column.key, data[column.key])
    db.session.commit()
    db.session.refresh(user)

    return user.to_dict()


def _delete_user(id):
    user = db.get_or_404(User, id)
    db.session.delete(user)
    db.session.commit()


app = Blueprint('user', __name__, url_prefix='/users')


@app.route('/', methods=['GET', 'POST'])
@jwt_required()
@requires_role('admin')
def list_or_create_user():
    if request.method == 'POST':
        _create_user()
        return {'message': 'The user was created!'}, HTTPStatus.CREATED
    else:
        return _list_users(), HTTPStatus.OK


@app.route('/<int:id>', methods=['GET'])
def get_user(id):
    if request.method == 'GET':
        return _get_user(id), HTTPStatus.OK


@app.route('/<int:id>/update', methods=['PATCH'])
def update_user(id):
    if request.method == 'PATCH':
        return _update_user(id), HTTPStatus.OK


@app.route('/<int:id>/delete', methods=['DELETE'])
def delete_user(id):
    if request.method == 'DELETE':
        _delete_user(id)
        return {'messsage': 'User deleted'}, HTTPStatus.NO_CONTENT
