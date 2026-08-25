from http import HTTPStatus

from src.app import db
from src.models.role import Role   

def test_create_role(client, admin_access_token):
    response = client.post(
        'roles/',
        headers = {'Authorization': f'Bearer {admin_access_token}'},
        json = {
            'name': 'batatinhas', 
        }
        )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {'message': 'The role was created!'}


def test_list_roles(client):
    response = client.get('roles/')
    roles = db.session.execute(db.select(Role)).scalars()

    assert response.status_code == HTTPStatus.OK
    assert response.json == {'roles': [ role.to_dict() for role in roles]}