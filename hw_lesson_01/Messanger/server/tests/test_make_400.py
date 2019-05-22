from datetime import datetime
from protocol import make_400

def test_make_400():
    request = {
        'time': datetime.now().timestamp(),
        'action': 'now',
        'data': 'Hello'
    }

    response = make_400(request)

    assert response.get("code") == 400