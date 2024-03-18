from json import dumps

from rest_framework.renderers import JSONRenderer


class BookmarkJSONRenderer(JSONRenderer):
    """Renderer for single bookmark object"""

    charset = "utf-8"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context is None:
            status_code = 200
        else:
            status_code = renderer_context.get("response").status_code

        # in case of DELETE request, the "data" will be None else "data" will hold queryset or error codes
        print("renderer data: ", data)
        if data is not None:
            errors = data.get("error", None)
        else:
            errors = None

        if errors is not None:
            return super(BookmarkJSONRenderer, self).render(data)
        else:
            return dumps({"status_code": status_code, "bookmark": data})


class BookmarksJSONRenderer(JSONRenderer):
    """Renderer for bookmark list"""

    charset = "utf-8"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context is None:
            status_code = 200
        else:
            status_code = renderer_context.get("response").status_code

        # request = renderer_context.get('request')
        # print('user: ', request.user)

        errors = data.get("error", None)
        # print('renderer data: ', data)

        # if 'total_bookmarks' in data:
        #         total_bookmarks = data.pop('total_bookmarks')
        # if 'bookmarks' in data:
        #         bookmarks = data.pop('bookmarks')
        #         data['data'] = bookmarks

        if errors is not None:
            return super(BookmarksJSONRenderer, self).render(data)
        else:
            return dumps({"status_code": status_code, "bookmarks": data})
