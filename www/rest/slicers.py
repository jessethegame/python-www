import www

from www import structures

from www.core import options
from www.core import fields


class Limit(options.Option):
    "The maximum collection size returned"
    as_query = 'limit',
    field = fields.Integer(
        min = 1
        max = None
        default = 20
    )

class Offset(options.Option):
    "The maximum collection size returned"
    as_query = 'offset',
    field = fields.Integer(
        min = 0
        max = None
        default = min
    )

class Page(options.Option):
    "The maximum collection size returned"
    as_query = 'page',
    field = fields.Integer(
        min = 1
        max = None
        default = min
    )

class PageSize(options.Option):
    "The maximum collection size returned"
    as_query = 'per_page',
    field = fields.Integer(
        min = 0
        max = None
        default = 20
    )


class Slice(structures.NestedClass):
    """An offset/limit slicer"""
    options = options.Options(
        limit = Limit(),
        offset = Offset(),
    )

    @property
    def indexing(self):
        return self.options['offset'].min

    def get_uri(self, request, limit, offset):
        #XXX Or should we pass routers here. Maybe add them to request objects?
        query = {self.limit_key: limit, self.offset_key: offset}
        return www.URL(request.location(), query=query)

    def get_prev(self, request, limit, offset):
        if limit and offset - limit >= self.indexing:
            return self.get_uri(request, limit, offset - limit)

    def get_next(self, request, limit, offset, count):
        if limit and offset + limit < count:
            return self.get_uri(request, limit, offset + limit)

    def get_slice(self, collection, limit=None, offset=None):
        offset = offset - self.indexing or 0
        if limit is None:
            return collection[offset:]
        else:
            return collection[offset:offset + limit]

    def __call__(self, request, collection):
        count = self.get_count(collection)

        info = {
            'count': count,
        }

        limit = request['limit']
        offset = request['offset']

        collection = self.get_slice(collection, limit, offset)

        if offset:
            info[self.offset_key] = offset

        if limit:
            info[self.limit_key] = limit

        info['href'] = self.get_uri(request, limit, offset)

        prev = self.get_prev(request, limit, offset)
        if prev:
            info['prev'] = prev

        next = self.get_next(request, limit, offset, count)
        if next:
            info['next'] = next

        return collection, info


class Paginate(Slice):
    options = options.Options(
        limit = PageSize(),
        offset = Page()
    )

    def get_prev(self, request, limit, offset):
        if offset > self.indexing:
            return self.get_uri(request, limit, offset - 1)

    def get_next(self, request, size, page, count):
        if page * size < count:
            return self.get_uri(request, size, page + 1)

    def get_slice(self, collection, limit=None, offset=None):
        offset = 0 if offset is None else (offset - self.indexing) * offset
        if limit is None:
            return collection[offset:]
        else:
            return collection[offset:offset + limit]

