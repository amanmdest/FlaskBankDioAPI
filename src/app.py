from datetime import datetime

import os
from typing import List
import click
import sqlalchemy as sa

from flask import Flask, current_app, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from sqlalchemy.orm import (
    DeclarativeBase, Mapped, mapped_column, relationship
    )


class Base(DeclarativeBase):
    metadata = sa.MetaData(naming_convention={
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })


db = SQLAlchemy(model_class=Base)
migrate = Migrate()
jwt = JWTManager()


class Role(db.Model): 
    __tablename__ = 'roles'

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(
        sa.String, nullable=False, unique=True
    )
    users: Mapped[List['User']] = relationship(back_populates='role')

    def __repr__(self) -> str:
        return f'Role(id={self.id!r}, \
            name={self.name!r})' 


class User(db.Model): 
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(
        sa.String, unique=True, nullable=False
        )
    password: Mapped[str] = mapped_column(sa.String, nullable=False)
    role_id: Mapped[int] = mapped_column(sa.ForeignKey('roles.id'))
    role: Mapped['Role'] = relationship(back_populates='users')
    # active: Mapped[bool] = mapped_column(sa.Boolean, default=True)

    def __repr__(self) -> str:
        return f'User(id={self.id!r}, \
            username={self.username!r}), \
            role={self.role!r}' 


class Post(db.Model): 
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    created: Mapped[datetime] = mapped_column(
        sa.DateTime, server_default=sa.func.now()
        )
    title: Mapped[str] = mapped_column(sa.String, nullable=False)
    body: Mapped[str] = mapped_column(sa.String, nullable=False)
    author_id: Mapped[int] = mapped_column(
        sa.ForeignKey('users.id'), nullable=False
        )

    def __repr__(self) -> str:
        return f'Post(id={self.id!r}, \
                title={self.title!r}, \
                author_id={self.author_id!r})'


@click.command('init-db')
def init_db_command():
    '''Clear the existing data and create new tables.'''
    global db
    with current_app.app_context():
        db.create_all()
    click.echo('Initialized the database.')


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///dio_bank.sqlite',
        JWT_SECRET_KEY='super-secret',
    )
    
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in 
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/olamundo/<usuario>/<int:idade>/<float:altura>')
    def hello_world(usuario, idade, altura):
        return {    
            'Usuário': usuario,
            'Idade': idade,
            'Altura': altura,
        }

    @app.route('/bemvindo')
    def bemvindo():
        return {'message': 'Bem vindo'}

    @app.route('/projects/')
    def projects():
        return '<p>The projects page</p>'

    @app.route('/about', methods=['POST', 'GET'])
    def about():
        if request.method == 'POST':
            return 'send me something mf, this should be a post'
        else:
            return '<p>The about page</p>'    

    with app.test_request_context():
        print(url_for(
            'hello_world', usuario='aman', idade=28, altura=1.65
            ))
        print(url_for('bemvindo'))
        print(url_for('projects'))
        print(url_for('about', next='/'))

    # register cli commands
    app.cli.add_command(init_db_command)

    # initialize extension
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    jwt.init_app(app)

    # register blueprints
    from src.controllers import user, auth, role # post

    app.register_blueprint(auth.app)
    app.register_blueprint(user.app)
    app.register_blueprint(role.app)

    return app