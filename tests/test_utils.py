import pytest

from src.utils import squared


@pytest.mark.parametrize('test_input, expected', 
[(4, 16), (3.0, 9), (8, 64), (7, 49)])
def test_squared_sucess(test_input, expected):
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