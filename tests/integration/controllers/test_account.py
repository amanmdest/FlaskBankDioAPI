from http import HTTPStatus

from sqlalchemy import func
from src.app import db
from src.models.account import Account


def test_create_account_success(admin_access_token, client, user):
    response = client.post(
        'accounts/',
        headers={'Authorization': f'Bearer {admin_access_token}'},
        json={
            'user_id': user.id,
            'holder': 'Sub-Zero',
            'balance': 400.000,
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {
        'account': {
           'balance': 400.0,
           'holder': 'Sub-Zero',
           'id': 7,
           'user_id': user.id,
       }}


def test_list_accounts_success(admin_access_token, client):
    response = client.get(
        'accounts/', headers={'Authorization': f'Bearer {admin_access_token}'}
    )
    accounts = db.session.execute(db.select(Account)).scalars()

    assert response.status_code == HTTPStatus.OK
    assert response.json == {'accounts': [
        account.to_dict() for account in accounts
        ]}


# def test_get_account_success(client):
#     response = client.get('accounts/1')

#     assert response.status_code == HTTPStatus.OK
#     assert response.json == {}


# def test_get_account_not_found(client):
#     response = client.get('accounts/54')

#     assert response.status_code == HTTPStatus.NOT_FOUND


# def test_update_user_success(client):
#     response = client.get('accounts/1')

#     assert response.status_code == HTTPStatus.OK
#     assert response.json == {}


# def test_delete_user_success(client):
#     response = client.get('accounts/1')

#     assert response.status_code == HTTPStatus.OK
#     assert response.json == {}
