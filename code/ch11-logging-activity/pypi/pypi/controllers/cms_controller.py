import logbook
from pyramid.httpexceptions import HTTPNotFound, HTTPFound
from pyramid.request import Request
from pyramid.view import view_config

from pypi.viewmodels.cms.cms_request_viewmodel import CmsRequestViewModel

log = logbook.Logger('CMS')


@view_config(route_name='cms_request', renderer='pypi:templates/cms/page.pt')
def cms_request(request: Request):
    vm = CmsRequestViewModel(request)
    if vm.page:
        log.trace(f'CMS request for page: {vm.page.title}')
        return vm.to_dict()

    if vm.redirect:
        log.trace(f'CMS request for redirect: {vm.redirect.short_url}')
        return HTTPFound(vm.redirect_url)

    log.info(f'CMS request not found: {vm.url}')

    raise HTTPNotFound()
