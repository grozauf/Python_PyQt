from routes import resolve

def test_resolve():
    controller = resolve('now')
    assert controller is not None

    controller = resolve('echo')
    assert controller is not None

    controller = resolve('bad_action')
    assert controller is None
