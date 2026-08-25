from http import HTTPStatus

from flask import Blueprint, request

from src.services.role import RoleServices

services = RoleServices

app = Blueprint('role', __name__, url_prefix='/roles')


@app.route('/', methods=['GET', 'POST'])
def list_or_create_role():
    if request.method == 'POST':
        services._create_role()
        return {'message': 'The role was created!'}, HTTPStatus.CREATED
    else:
        return {'roles': services._list_roles()}, HTTPStatus.OK
