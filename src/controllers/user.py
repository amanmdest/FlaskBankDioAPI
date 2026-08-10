from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from sqlalchemy import inspect
from src.app import User, db
from http import HTTPStatus

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

def _list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars()
    result = [{
        'id': user.id, 
        'username': user.username,
        'role': {'id': user.role.id,'name': user.role.name}
        } for user in users]
    return result

def _get_user(id):
    user = db.get_or_404(User, id)
    return {
        'id': user.id, 
        'username': user.username, 
        'role': {'id': user.role.id,'name': user.role.name}
        }

def _update_user(id):
    data = request.json
    user = db.get_or_404(User, id)
    # print(user)
    mapper = inspect(User)
    for column in mapper.attrs:
        # print(column.key)
        if column.key in data:
            setattr(user, column.key, data[column.key])    
    db.session.commit()

    return {
        "id": user.id,
        "username": user.username,
        'role': {'id': user.role.id,'name': user.role.name}
    }

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
        return {
            'message': 'The user was created!'
            }, HTTPStatus.CREATED
    else: 
        return {
            'users': _list_users()
            }, HTTPStatus.OK


@app.route('/<int:id>', methods=['GET'])
def get_user(id): 
    if request.method == 'GET':
        return {'users': _get_user(id)}, HTTPStatus.OK


@app.route('/<int:id>/update', methods=['PATCH'])
def update_user(id): 
    if request.method == 'PATCH':
        return _update_user(id), HTTPStatus.OK


@app.route('/<int:id>/delete', methods=['DELETE'])
def delete_user(id): 
    if request.method == 'DELETE':
        _delete_user(id)
        return {"messsage": "User deleted"}, HTTPStatus.NO_CONTENT