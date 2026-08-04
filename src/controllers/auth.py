from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from src.app import User, db

app = Blueprint('auth', __name__, url_prefix='/auth')


@app.route('/login', methods=['POST'])
def _login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    query = db.select(User).where(User.username == username)
    user = db.session.execute(query).scalar()

    if not user or user.password != password:
        return {"message": "Bad username or password"}, HTTPStatus.UNAUTHORIZED

    access_token = create_access_token(identity=str(user.id))
    return {"access_token": access_token}


@app.route('/protected', methods=['GET'])
@jwt_required()
def _protected():
    current_user = get_jwt_identity()
    return {"logged_in_as": current_user}, HTTPStatus.OK