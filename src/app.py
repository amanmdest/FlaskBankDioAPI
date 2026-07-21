from flask import Flask, url_for, request

app = Flask(__name__)


@app.route('/olamundo/<usuario>/<int:idade>/<float:altura>')
def hello_world(usuario, idade, altura):
    print(f'{type(usuario)}')
    print(f'{type(idade)}')
    print(f'{type(altura)}')
    return f'<h1>Hello, world! usuário: {usuario.upper()}</h1>'


@app.route('/bemvindo')
def bemvindo():
    return '<h1>Bem vindo</h1>'


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