from datetime import datetime
from protocol import validate_request

def test_make_400():
    request = {
        'time': datetime.now().timestamp(),
        'action': 'now',
        'user': 'User'
    }

    is_valid = validate_request(request)

    assert is_valid == True

    request = {'user': 'User'}

    is_valid = validate_request(request)

    assert is_valid == False
