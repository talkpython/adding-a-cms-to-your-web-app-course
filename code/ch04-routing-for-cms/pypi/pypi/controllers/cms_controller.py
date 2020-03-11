from pyramid.request import Request
from pyramid.response import Response
from pyramid.view import view_config


@view_config(route_name='cms_request')  # , renderer='pypi:templates/home/index.pt')
def cms_request(request: Request):
    sub_path = request.matchdict.get('sub_path')
    url = '/'.join(sub_path)
    return Response(body=f"Hello CMS: You requested {url}")
