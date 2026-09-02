from http import HTTPStatus

import pytest

from src.utils import requires_role, squared


@pytest.mark.parametrize(
    'test_input, expected',  # noqa
    [(4, 16), (3.0, 9), (8, 64), (7, 49)],
)
def test_squared_success(test_input, expected):
    result = squared(test_input)

    assert result == expected


@pytest.mark.parametrize(
    'test_input, exc_class, msg',  # noqa
    [
        (
            'a',
            TypeError,
            "unsupported operand type(s) for ** or pow(): 'str' and 'int'",
        ),
        (
            None,
            TypeError,
            "unsupported operand type(s) for ** or pow(): \
'NoneType' and 'int'",
        ),
    ],
)
def test_squared_fail(test_input, exc_class, msg):
    with pytest.raises(exc_class) as exc:
        squared(test_input)

    assert str(exc.value) == msg


def test_required_role_success(mocker):
    user_mock = mocker.Mock()
    user_mock.role.name = 'admin'

    mocker.patch('src.utils.get_jwt_identity')
    mocker.patch('src.utils.db.get_or_404', return_value=user_mock)

    decorated_function = requires_role('admin')(lambda: 'success')
    result = decorated_function()

    assert result == 'success'


def test_required_role_fail(mocker):
    user_mock = mocker.Mock()
    user_mock.role.name = 'normal'

    mocker.patch('src.utils.get_jwt_identity')
    mocker.patch('src.utils.db.get_or_404', return_value=user_mock)

    decorated_function = requires_role('admin')(lambda: 'success')
    result = decorated_function()

    assert result == (
        {'message': 'Current user does not have access'},
        HTTPStatus.FORBIDDEN,
    )
