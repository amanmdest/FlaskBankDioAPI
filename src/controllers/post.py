from flask import Blueprint
# from src.app import Post, db
# from http import HTTPStatus

app = Blueprint('post', __name__, url_prefix='/posts')