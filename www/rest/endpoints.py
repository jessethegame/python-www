from www.server.endpoints import Endpoint
from www.server import responses

from www.core.options import Options, Option
from www.core.fields import String


class Endpoint(Endpoint):
    def envelope(self, status, meta):
        return lambda body: {'code': status, 'meta': meta, 'data': body}

    @property
    def schemas(self):
        return self.resource.schemas

class One(Endpoint):
    methods = {'GET', 'DELETE', 'PUT', 'PATCH'}

    options = Options(
        identifier = Option(
            as_kwarg = 'uid',
            field = String(
                help_text = "A unique identifier without a slash",
                required = True,
            )
        )
    )

    @property
    def schemas(self):
        return self.resource.schemas['entity']

    @property
    def name(self):
        return self.resource.name + '.one'

    def GET(self, request):
        "Return an identified entity"
        return self.resource.fetch(request['identifier'])

    def PATCH(self, request):
        "Update an identified entity"
        return self.resource.update(request['identifier'], request['data'])

    def DELETE(self, request):
        "Delete an identified entity"
        self.resource.delete(request['identifier'])

    def PUT(self, request):
        "Replace or create an entity"
        return self.resource.replace(request['identifier'], request['data'])


class Few(Endpoint):
    methods = {'GET', 'DELETE', 'PUT', 'PATCH'}

    options = Options(
        identifier = Option(
            as_kwarg = 'uids',
            field = String(
                help_text = "A list of identifiers without a slash",
                required = True,
            )
        )
    )

    @property
    def schemas(self):
        return self.resource.schemas['entity']

    @property
    def name(self):
        return self.resource.name + '.few'

    def GET(self, request):
        "Return the identified collection"
        return tuple(self.resource.fetch(i) for i in request['identifier'])

    def DELETE(self, request):
        "Delete an identified collection"
        for i in request['identifier']:
            self.resource.delete(i)

    def PUT(self, request):
        "Replace or create a collection"
        raise responses.NotImplemented

    def PATCH(self, request):
        "Update an identified collection"
        raise responses.NotImplemented


class All(Endpoint):
    methods = {'GET', 'POST', 'DELETE', 'PATCH'}

    @property
    def schemas(self):
        return self.resource.schemas['collection']

    @property
    def name(self):
        return self.resource.name

    def POST(self, request):
        "Append a new entity or collection"
        uid = self.resource.create(request['data'])
        #TODO put the reverse/location function in the proper place
        location = request['router'].reverse(self.name + '.one', uid=uid)
        raise responses.Created(request, location=location)

    def GET(self, request):
        "Return a filtered collection"
        objects = self.resource.query(request)
        return self.resource.slice(objects)

    def PATCH(self, request):
        "Update each element a filtered collection with the same patch"
        objects = self.resource.query(request)
        self.resource.batch(request, objects)

    def DELETE(self, request):
        "Delete a filtered collection"
        self.resource.drop(request)

