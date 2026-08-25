from flask import request
from sqlalchemy import inspect

from src.app import db
from src.models.user import User


class UserServices:
    def _create_user():
        data = request.json
        user = User(
            username=data['username'],
            password=data['password'],
            role_id=data['role_id'],
        )
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)

    def _list_users():
        query = db.select(User)
        users = db.session.execute(query).scalars()
        result = [user.to_dict() for user in users]
        return result

    def _get_user(id):
        user = db.get_or_404(User, id)
        return user.to_dict()

    def _update_user(id):
        data = request.json
        user = db.get_or_404(User, id)
        # print(user)
        mapper = inspect(User)
        # for column in mapper.attrs:
        for column in mapper.columns:
            # print(column.key)
            if column.key in data:
                setattr(user, column.key, data[column.key])
        db.session.commit()
        db.session.refresh(user)

        return user.to_dict()

    def _delete_user(id):
        user = db.get_or_404(User, id)
        db.session.delete(user)
        db.session.commit()
