# from flask import Blueprint, redirect, request, url_for
# from sqlalchemy import inspect
# from src.app import Post, db
# from http import HTTPStatus


# def _create_post():
#     data = request.json
#     post = Post(postname=data['postname'])
#     db.session.add(post)
#     db.session.commit()


# def _list_post():
#     query = db.select(Post)
#     posts = db.session.execute(query).scalars()
#     result = [{'id': post.id, 'postname': post.postname} for post in posts]
#     return result


# def _get_post(id):
#     post = db.get_or_404(Post, id)
#     return {'id': post.id, 'postname': post.postname}


# def _update_post(id):
#     data = request.json
#     post = db.get_or_404(Post, id)
#     # print(post)
#     mapper = inspect(Post)
#     for column in mapper.attrs:
#         # print(column.key)
#         if column.key in data:
#             setattr(post, column.key, data[column.key])    
#     db.session.commit()

#     return {
#         "id": post.id,
#         "postname": post.postname
#     }


# def _delete_post(id):
#     post = db.get_or_404(Post, id)
#     db.session.delete(post)
#     db.session.commit()


# app = Blueprint('post', __name__, url_prefix='/posts')


# @app.route('/', methods=['GET', 'POST'])
# def list_or_create_post(): 
#     if request.method == 'POST':
#         _create_post()
#         return {'message': 'The post was created!'}, HTTPStatus.CREATED
#     else: 
#         return {'posts': _list_post()}, HTTPStatus.OK


# @app.route('/<int:id>', methods=['GET'])
# def get_post(id): 
#     if request.method == 'GET':
#         return {'posts': _get_post(id)}, HTTPStatus.OK


# @app.route('/<int:id>/update', methods=['PATCH'])
# def update_post(id): 
#     if request.method == 'PATCH':
#         return _update_post(id), HTTPStatus.OK


# @app.route('/<int:id>/delete', methods=['DELETE'])
# def delete_post(id): 
#     if request.method == 'DELETE':
#         _delete_post(id)
#         return {"messsage": "Post deleted"}, HTTPStatus.NO_CONTENT