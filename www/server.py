import www.http

class Request(www.http.Request):
    def

class WSGIRequest(Request):
    def __init__(self, env):
        meta = {}
        headers = {}

        method = env.pop('REQUEST_METHOD')
        url = env.pop('PATH')
        query_string = env.pop('QUERY_STRING')

        headers['content-length'] = env.pop('CONTENT_LENGTH')
        headers['content-type'] = env.pop('CONTENT_TYPE')

        body = env.pop('wsgi.input')

        for key in (
            #'CONTENT_TYPE',
            #'CONTENT_LENGTH',
            'DOCUMENT_ROOT',
            #'HTTP_COOKIE',
            #'HTTP_HOST',
            #'HTTP_REFERER',
            #'HTTP_USER_AGENT',
            'HTTPS',
            #'PATH',
            #'QUERY_STRING',
            'REMOTE_ADDR',
            'REMOTE_HOST',
            'REMOTE_PORT',
            'REMOTE_USER',
            'REQUEST_METHOD',
            'REQUEST_URI',
            'SCRIPT_FILENAME',
            'SCRIPT_NAME',
            'SERVER_ADMIN',
            'SERVER_NAME',
            'SERVER_PORT',
            'SERVER_SOFTWARE',
        ):
            meta[key] = env.pop(key)


        for key, val in env.items():
            # Remove 'HTTP_' from keys, then lower and replace '_' by '-'
            headers[key[5:].lower().replace('_', '-')] = val

        super().__init__(url=url, method=method, body=body, headers=headers,
                meta=meta, query_string=query_string, **kwargs)

