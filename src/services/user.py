from http import HTTPStatus

from flask import abort, request
from sqlalchemy import inspect

from src.app import db
from src.models.role import Role
from src.models.user import User


class UserServices:
    def _create_user():
        data = request.json
        roles = db.session.execute(db.select(Role.id)).scalars().all()
        if data['role_id'] not in roles:
            # abort() automatically returns the right status code to Flask
            abort(HTTPStatus.NOT_FOUND)

        user = User(
            username=data['username'],
            password=data['password'],
            role_id=data['role_id'],
        )
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)

    def _list_users():
        users = db.session.execute(db.select(User)).scalars()
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
