import os
import click

from flask import Flask, current_app, url_for, request

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    global db
    with current_app.app_context():
        db.create_all()
    click.echo('Initialized the database.')


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///dio_bank.sqlite',
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

    return app