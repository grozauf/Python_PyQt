from datetime import datetime
from protocol import make_404

def test_make_404():
    request = {
        'time': datetime.now().timestamp(),
        'action': 'now',
        'data': 'Hello'
    }

    response = make_404(request)

    assert response.get("code") == 404