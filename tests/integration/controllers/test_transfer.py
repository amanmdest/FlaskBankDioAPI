from http import HTTPStatus

from src.app import db
from src.models.transfer import Transfer


def test_make_transfer_success(admin_access_token, client, account):
    old_balance = account.balance
    response = client.post(
        f'transfers/{account.id}',
        headers={'Authorization': f'Bearer {admin_access_token}'},
        json={
            'amount': 148,
            'transfer_type': 'withdraw',
            'description': 'health',
        },
    )

    response2 = client.get(f'accounts/{account.id}')

    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {
        'transfer': {
            'account_id': 2,
            'amount': 148.0,
            'description': 'health',
            'id': 5,
        },
    }
    assert response2.json['balance'] < old_balance


def test_make_transfer_solde_insuffisant(admin_access_token, client, account):
    old_balance = account.balance
    response = client.post(
        f'transfers/{account.id}',
        headers={'Authorization': f'Bearer {admin_access_token}'},
        json={
            'amount': 14800.0,
            'transfer_type': 'withdraw',
            'description': 'health',
        },
    )
    response2 = client.get(f'accounts/{account.id}')

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json[
        'description'] == "you don't have enough \
                    money for that operation"
    assert response2.json['balance'] == old_balance


def test_list_transfers_success(client):
    response = client.get('transfers/')
    transfers = db.session.execute(db.select(Transfer)).scalars()

    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        'transfers': [transfer.to_dict() for transfer in transfers]
    }


def test_list_transfers_by_account_success(client, transfer):
    response = client.get(f'transfers/account/{transfer.account_id}')
    query = db.select(Transfer).where(
        Transfer.account_id == transfer.account_id)
    transfers = db.session.execute(query).scalars()

    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        'transfers': [transfer.to_dict() for transfer in transfers]
    }


def test_get_transfer_success(client, transfer):
    response = client.get(f'transfers/{transfer.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json == transfer.to_dict()


def test_get_transfer_not_found(client):
    response = client.get('transfers/57')

    assert response.status_code == HTTPStatus.NOT_FOUND
