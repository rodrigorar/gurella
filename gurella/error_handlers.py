def handler_bad_request(e):
    return 'Bad Request', 400


def handler_internal_server_error(e):
    return 'Internal Server Error', 500
