from flask import Blueprint, redirect, request, url_for
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import inspect
from src.app import Role, db
from http import HTTPStatus


def _create_role():
    data = request.json
    role = Role(name=data['name'])
    db.session.add(role)
    db.session.commit()


def _list_roles():
    query = db.select(Role)
    roles = db.session.execute(query).scalars()
    result = [{
        'id': role.id, 'name': role.name, 'users': [{
            'id': user.id,
            'username': user.username
            } for user in role.users]
        } for role in roles]
    
    return result


app = Blueprint('role', __name__, url_prefix='/roles')


@app.route('/', methods=['GET', 'POST'])
def list_or_create_role(): 
    if request.method == 'POST':
        _create_role()
        return {
            'message': 'The role was created!'
            }, HTTPStatus.CREATED
    else: 
        return {
            'roles': _list_roles()
            }, HTTPStatus.OK
