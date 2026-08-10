from http import HTTPStatus
from unittest.mock import Mock, patch
import pytest

from src.utils import requires_role, squared


@pytest.mark.parametrize('test_input, expected', 
[(4, 16), (3.0, 9), (8, 64), (7, 49)])
def test_squared_success(test_input, expected):
    result = squared(test_input)

    assert result == expected


@pytest.mark.parametrize('test_input, exc_class, msg', 
[('a', TypeError, 
  "unsupported operand type(s) for ** or pow(): 'str' and 'int'"),
(None, TypeError, 
 "unsupported operand type(s) for ** or pow(): 'NoneType' and 'int'")
 ])
def test_squared_fail(test_input, exc_class, msg):
    with pytest.raises(exc_class) as exc:
        squared(test_input) 
    
    assert str(exc.value) == msg


def test_required_role_success():
    user_mock = Mock()
    user_mock.role.name = 'admin'

    get_jwt_identity_mock = patch('src.utils.get_jwt_identity')
    db_get_or_404_mock = patch('src.utils.db.get_or_404', return_value=user_mock)
    db_get_or_404_mock.start()
    get_jwt_identity_mock.start()

    decorated_function = requires_role('admin')(lambda: 'success')
    result = decorated_function()

    assert result == 'success'

    db_get_or_404_mock.stop()
    get_jwt_identity_mock.stop()


def test_required_role_fail():
    user_mock = Mock()
    user_mock.role.name = 'normal'

    get_jwt_identity_mock = patch('src.utils.get_jwt_identity')
    db_get_or_404_mock = patch('src.utils.db.get_or_404', return_value=user_mock)
    db_get_or_404_mock.start()
    get_jwt_identity_mock.start()

    decorated_function = requires_role('admin')(lambda: 'success')

    result = decorated_function()

    assert result == (
        {'message': "Current user doesn't have access"}, HTTPStatus.FORBIDDEN
    )

    db_get_or_404_mock.stop()
    get_jwt_identity_mock.stop()