import pytest

from src.models.account import Account
from src.models.transfer import Transfer
from src.models.user import User
from src.models.role import Role
from src.app import create_app, db


@pytest.fixture(scope='session')
def app():
    app = create_app({
        'SECRET_KEY': 'test',
        'SQLALCHEMY_DATABASE_URI': 'sqlite://',
        'JWT_SECRET_KEY': 'test',
    })

    print("\n--- ROTAS REGISTRADAS NO TESTE ---")
    for rule in app.url_map.iter_rules():
        print(f"Métodos: {rule.methods} -> Caminho: {rule.rule}")
    print("----------------------------------\n")


    with app.app_context():
        db.create_all()
        _populate_initial_data()
        yield app
        db.drop_all()


def _populate_initial_data(): 
    roles = [
        Role(id=1, name='admin'),
        Role(id=2, name='normal')
    ]

    db.session.add_all(roles)
    db.session.commit()

    users = [
        User(id=1, username='Liu Kang', password='guaaa', role_id=1),
        User(id=2, username='Johnny Cage', password='123', role_id=2),
        User(id=3, username='Sub Zero', password='abc', role_id=2)
    ]
    db.session.add_all(users)
    db.session.commit()

    accounts = [
        Account(user_id=1, holder='Revolver Ocelot', balance=45),
        Account(user_id=1, holder='The End', balance=666),
        Account(user_id=2, holder='Jake Gyllenhaal', balance=777),
        Account(user_id=2, holder='Princess Farah', balance=994),
        Account(user_id=3, holder='Ezio Auditore', balance=2.50),
        Account(user_id=3, holder='Evie Frye', balance=198),
    ]
    db.session.add_all(accounts)
    db.session.commit()

    transfers = [
        Transfer(account_id=1, 
            amount=2000, 
            transfer_type='deposit', 
            description='guarda-roupa'),
        Transfer(account_id=6,
            amount=13, 
            transfer_type='withdraw', 
            description='açaí'),
        Transfer(account_id=5,
            amount=89,
            transfer_type='deposit',
            description='compact cd player'),
        Transfer(account_id=3,
            amount=2,
            transfer_type='withdraw',
            description='chiclete'),
    ]
    db.session.add_all(transfers)
    db.session.commit()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def user():
    return db.session.get(User, 1)


@pytest.fixture
def account():
    return db.session.get(Account, 2)


@pytest.fixture
def admin_access_token(client, user):
    response = client.post(
        '/auth/login',
        json={'username': user.username, 'password': user.password},
    )

    return response.json['access_token']
