from functools import reduce
from settings import INSTALLED_MODULES


def get_server_routes():
    return reduce(
        lambda value, item: value + [getattr(item, 'routes', None)],
        reduce(
            lambda value, item: value + [getattr(item, 'routes', None)],
            reduce(
                lambda value, item: value + [__import__(f'{ item }.routes')],
                INSTALLED_MODULES,
                []
            ),
            []
        ),
        []
    )


def resolve(action, routes=None):
    routes_mapping = {}
    for controller_route in routes or get_server_routes():
        for route in controller_route:
            routes_mapping[route['action']] = route['controller']
    return routes_mapping.get(action, None)