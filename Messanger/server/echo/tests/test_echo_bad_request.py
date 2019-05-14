from datetime import datetime

from echo.controllers import get_echo

def test_echo_bad_request():
    request = {
        'time': datetime.now().timestamp(),
        'action': 'now'
    }

    response = get_echo(request)

    assert response.get('code') == 400
