from http import HTTPStatus

from src.app import db
from src.models.user import User

# def test_create_user_success(admin_access_token, client):
#     role_id = db.session.execute(
#         db.select(Role.id).where(Role.name == 'admin')
#     ).scalar()

#     response = client.post(
#         'users/',
#         headers={'Authorization': f'Bearer {admin_access_token}'},
#         json={
#             'username': 'Snake Eater',
#             'password': 'notforhonor',
#             'role_id': role_id,
#         },
#     )

#     assert response.status_code == HTTPStatus.CREATED
#     assert response.json == {'message': 'The user was created!'}
#     assert db.session.execute(db.select(func.count(User.id))).scalar() == 4  # noqa


def test_create_user_unexisting_role(admin_access_token, client):
    response = client.post(
        'users/',
        headers={'Authorization': f'Bearer {admin_access_token}'},
        json={
            'username': 'Solid Snake',
            'password': 'butforyou',
            'role_id': 7
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == {'message': 'The requested resource was not found'}


def test_list_users_success(admin_access_token, client):
    response = client.get(
        'users/', headers={'Authorization': f'Bearer {admin_access_token}'}
    )
    users = db.session.execute(db.select(User)).scalars()

    assert response.status_code == HTTPStatus.OK
    assert response.json == [user.to_dict() for user in users]


def test_get_user_success(client, user):
    response = client.get('users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json == user.to_dict()


def test_get_user_not_found(client):
    response = client.get('users/54')

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_user_success(client, user, admin_access_token):
    response = client.patch(
        f'users/{user.id}',
        headers={'Authorization': f'Bearer {admin_access_token}'},
        json={
            'username': 'Shalashaska'
            })

    assert response.status_code == HTTPStatus.OK
    assert response.json == {
       'accounts': [
           2,
           7,
       ],
       'id': 1,
       'role': 'admin',
       'username': 'Shalashaska',
   }


# def test_update_user_unexisting_role(client, user, admin_access_token):
#     response = client.patch(
#         f'users/{user.id}',
#         headers={'Authorization': f'Bearer {admin_access_token}'},
#         json={
#             'username': 'Shalashaska',
#             'role_id': 32
#             })

#     assert response.status_code == HTTPStatus.OK
#     assert response.json == {
#        'accounts': [
#            2,
#            7,
#        ],
#        'id': 1,
#        'role': 'admin',
#        'username': 'Shalashaska',
#    }


# def test_delete_user_success(client):
#     response = client.get('users/1')

#     assert response.status_code == HTTPStatus.OK
#     assert response.json == {}
