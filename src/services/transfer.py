from http import HTTPStatus

from flask import abort, request

from src.app import db
from src.models.account import Account
from src.models.transfer import Transfer
from src.services.account import AccountServices

acc_services = AccountServices


class TransferServices:
    def _make_transfer(account_id):
        query = db.select(Account).where(Account.id == account_id)
        account = db.session.execute(query).scalar()
        data = request.json

        if data['transfer_type'] == 'withdraw':
            if account.balance < data['amount']:
                abort(
                    HTTPStatus.FORBIDDEN,
                    description="you don't have enough \
                    money for that operation"
                )

            account_data = {'balance': account.balance - data['amount']}

        if data['transfer_type'] == 'deposit':
            account_data = {'balance': account.balance + data['amount']}

        acc_services._update_account(account_id, account_data)

        transfer = Transfer(
            account_id=account.id,
            amount=data['amount'],
            transfer_type=data['transfer_type'],
            description=data['description'],
        )

        db.session.add(transfer)
        db.session.commit()

        return transfer.to_dict()

    def _list_transfers():
        query = db.select(Transfer)
        transfer = db.session.execute(query).scalars()
        result = [transfer.to_dict() for transfer in transfer]
        return result

    def _list_transfers_by_account(account_id):
        query = db.select(Transfer).where(Transfer.account_id == account_id)
        transfer = db.session.execute(query).scalars()
        result = [transfer.to_dict() for transfer in transfer]
        return result

    def _get_transfer(id):
        transfer = db.get_or_404(Transfer, id)

        return transfer.to_dict()
