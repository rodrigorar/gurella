from flask import request


def handler_exception(e):
    if request.path.startswith('/api/'):
        return '{"message": "Internal Server Error"}'
    return 'You fucked up'
