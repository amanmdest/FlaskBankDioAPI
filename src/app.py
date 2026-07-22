import os

from flask import Flask, url_for, request


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE='dio_bank.sqlite',
    )
    
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile(
            'config.py', 
            silent=True
        )
    else:
        # load the test config if passed in 
        app.config.from_mapping(test_config)

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

    from . import db
    db.init_app(app)

    return app