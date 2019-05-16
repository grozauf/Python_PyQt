from datetime import datetime

from echo.controllers import get_echo

def test_get_echo():
    request = {
        'time': datetime.now().timestamp(),
        'action': 'now',
        'data': 'Hello'
    }

    response = get_echo(request)

    assert response.get('data') == 'Hello'

