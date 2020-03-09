from pyramid.httpexceptions import HTTPNotFound, HTTPFound
from pyramid.request import Request
from pyramid.view import view_config

from pypi.viewmodels.cms.page_viewmodel import CMSRequestViewModel


@view_config(route_name='cms_request', renderer='pypi:templates/cms/page.pt')
def cms_request(request: Request):
    vm = CMSRequestViewModel(request)
    if vm.page:
        return vm.to_dict()
    elif vm.redirect:
        return HTTPFound(vm.redirect.url)

    return HTTPNotFound()
