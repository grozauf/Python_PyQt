from datetime import datetime
from jim import pack, unpack

def test_pack_unpack():
    request = {
        'time': datetime.now().timestamp(),
        'action': 'now',
        'data': 'Hello'
    }

    b_request = pack(request)
    request = unpack(b_request)

    assert request.get('action') == 'now'
    assert request.get('data') == 'Hello'
