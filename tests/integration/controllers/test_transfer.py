from http import HTTPStatus

from src.app import db
from src.models.transfer import Transfer


def test_make_transfer_success(admin_access_token, client, account):
    response = client.post(
        f'transfers/{account.id}',
        headers={'Authorization': f'Bearer {admin_access_token}'},
        json={
            'amount': 148,
            'transfer_type': 'withdraw',
            'description': 'health',
        },
    )
    
    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {}


def test_list_transfers_success(client):
    response = client.get('transfers/')
    transfers = db.session.execute(db.select(Transfer)).scalars()

    assert response.status_code == HTTPStatus.OK
    assert response.json == {'transfers': [
        transfer.to_dict() for transfer in transfers
        ]}


# def test_get_transfer_success(client, user):
#     response = client.get(f'transfers/{user.id}')
#     transfer = db.session.execute(
#         db.select(Account).where(Account.account_id == user.id)
#         ).scalar()
    
#     assert response.status_code == HTTPStatus.OK
#     assert response.json == {
#         'account_id': transfer.account_id,
#         'holder': transfer.holder, 
#         'balance': transfer.balance,
#         'id': transfer.id
#     }


# def test_get_transfer_not_found(client):
#     response = client.get('transfers/54')

#     assert response.status_code == HTTPStatus.NOT_FOUND