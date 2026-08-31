from flask import request

from src.app import db
from src.models.role import Role


class RoleServices:
    def _create_role():
        data = request.json
        role = Role(name=data['name'])
        db.session.add(role)
        db.session.commit()

    def _list_roles():
        query = db.select(Role)
        roles = db.session.execute(query).scalars()
        result = [role.to_dict() for role in roles]

        return result
