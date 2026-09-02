from flask import request
from sqlalchemy import inspect

from src.app import db
from src.models.account import Account


class AccountServices:
    def _create_account():
        data = request.json
        account = Account(
            user_id=data['user_id'],
            holder=data['holder'],
            balance=data['balance'],
        )

        db.session.add(account)
        db.session.commit()
        db.session.refresh(account)

        return account.to_dict()

    def _list_accounts():
        query = db.select(Account)
        accounts = db.session.execute(query).scalars()
        result = [account.to_dict() for account in accounts]

        return result

    def _get_account(id):
        account = db.get_or_404(Account, id)

        return account.to_dict()

    def _update_account(id, data_to_update=None):
        data = data_to_update if data_to_update is not None else request.json

        account = db.get_or_404(Account, id)
        mapper = inspect(Account)

        for column in mapper.columns:
            if column.key in data:
                setattr(account, column.key, data[column.key])

        db.session.commit()
        db.session.refresh(account)

        return account.to_dict()

    def _delete_account(id):
        account = db.get_or_404(Account, id)

        db.session.delete(account)
        db.session.commit()
