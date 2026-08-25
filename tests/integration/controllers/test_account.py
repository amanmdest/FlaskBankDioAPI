from http import HTTPStatus

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


def test_get_account_success(client, user):
    response = client.get(f'accounts/{user.id}')
    account = db.session.execute(
        db.select(Account).where(Account.user_id == user.id)
        ).scalar()
    
    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        'user_id': account.user_id,
        'holder': account.holder, 
        'balance': account.balance,
        'id': account.id
    }


def test_get_account_not_found(client):
    response = client.get('accounts/54')

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_account_success(client, admin_access_token, user):
    response = client.patch(
        f'accounts/{user.id}',
        headers={'Authorization': f'Bearer {admin_access_token}'},
        json={
            'user_id': user.id,
            'holder': 'Scorpion',
            'balance': 450.0,
           }
        )
    account = db.session.execute(
        db.select(Account).where(Account.user_id == user.id)
        ).scalar()

    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        'balance': account.balance,
        'holder': account.holder,
        'id': account.id,
        'user_id': user.id,
    }


def test_update_account_not_found(client, admin_access_token, user):
    response = client.patch(
        'accounts/13',
        headers={'Authorization': f'Bearer {admin_access_token}'},
        json={
            'user_id': user.id,
            'holder': 'Scorpion',
            'balance': 450.0,
           }
        )
    
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == {'message': 'The requested resource was not found'}


def test_delete_account_success(client, admin_access_token, user):
    response = client.delete(
        f'accounts/{user.id}',
        headers={'Authorization': f'Bearer {admin_access_token}'}
    )
    
    assert response.status_code == HTTPStatus.OK
    assert response.json == {'message': 'Account deleted'}
