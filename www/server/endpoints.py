"""
Endpoints define the behaviour of http methods on a resource.

A suggested usage pattern is to have resources use fixed interfaces
to make endpoints agnostic and resources pluggable.
"""

class Endpoint(layers.Layer):
    # The methods that are allowed on this endpoint
    methods = www.methods.ALL

    def __init__(self, resource):
        self.resource = resource

    def GET(self, request):
        raise www.NotImplemented

    def POST(self, request):
        raise www.NotImplemented

    def PUT(self, request):
        raise www.NotImplemented

    def DELETE(self, request):
        raise www.NotImplemented

    def PATCH(self, request):
        raise www.NotImplemented

    #XXX This is a very naive solution that might run heavy
    #    lookups/logic unnecessarily
    def HEAD(self, request):
        self.GET(request)
        return None

    #XXX Somehow this should find all available options and add them to the
    #    response. The adding of the options metadata could be responsibility
    #    of the options.Option class, this method would then only need to
    #    add them to the response body
    def OPTIONS(self, request):
        response = responses.NoContent()
        response['Allow'] = ', '.join(self.methods)
        raise response

    def call(self, request):
        if not request['method'] in self.methods:
            raise www.MethodNotAllowed

        return getattr(self, request['method'])(request)

