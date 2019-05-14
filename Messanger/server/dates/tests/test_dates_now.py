from datetime import datetime

from dates.controllers import get_date_now


def test_get_date_now():
    date = datetime.now()
    s_date = date.strftime('%Y.%m.%d')

    request = {
        'time': datetime.now().timestamp(),
        'action': 'now'
    }

    response = get_date_now(request)

    assert response.get('data') == s_date