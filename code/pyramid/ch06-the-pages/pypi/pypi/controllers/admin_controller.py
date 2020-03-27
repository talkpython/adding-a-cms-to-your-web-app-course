from pyramid.httpexceptions import HTTPFound
from pyramid.request import Request
from pyramid.view import view_config

from pypi.infrastructure import permissions
from pypi.services import cms_service
from pypi.viewmodels.admin.editpage_viewmodel import EditPageViewModel
from pypi.viewmodels.admin.editredirect_viewmodel import EditRedirectViewModel
from pypi.viewmodels.admin.pagelist_viewmodel import PagesListViewModel
from pypi.viewmodels.admin.redirectlist_viewmodel import RedirectListViewModel
from pypi.viewmodels.shared.viewmodel_base import ViewModelBase


@view_config(route_name='admin_index', renderer='pypi:templates/admin/index.pt')
@permissions.admin
def index(request: Request):
    vm = ViewModelBase(request)
    return vm.to_dict()


@view_config(route_name='redirects', renderer='pypi:templates/admin/redirects.pt')
@permissions.admin
def redirects(request: Request):
    vm = RedirectListViewModel(request)
    return vm.to_dict()


@view_config(route_name='pages', renderer='pypi:templates/admin/pages.pt')
@permissions.admin
def pages(request: Request):
    vm = PagesListViewModel(request)
    return vm.to_dict()


#################################################
#       ADD PAGE
#
@view_config(route_name='add_page',
             request_method='GET',
             renderer='pypi:templates/admin/edit_page.pt')
@permissions.admin
def add_page_get(request: Request):
    vm = EditPageViewModel(request)
    return vm.to_dict()


@view_config(route_name='add_page',
             request_method='POST',
             renderer='pypi:templates/admin/edit_page.pt')
@permissions.admin
def add_page_post(request: Request):
    return add_or_edit_page(request)


#################################################
#       EDIT PAGE
#
@view_config(route_name='edit_page',
             request_method='GET',
             renderer='pypi:templates/admin/edit_page.pt')
@permissions.admin
def edit_page_get(request: Request):
    vm = EditPageViewModel(request)
    return vm.to_dict()


@view_config(route_name='edit_page',
             request_method='POST',
             renderer='pypi:templates/admin/edit_page.pt')
@permissions.admin
def edit_page_post(request: Request):
    return add_or_edit_page(request)


def add_or_edit_page(request: Request):
    vm = EditPageViewModel(request)

    vm.process_form()
    if vm.error:
        return vm.to_dict()

    if vm.page_id:
        cms_service.update_page(vm.page_id, vm.title, vm.url, vm.contents)
    else:
        cms_service.create_page(vm.title, vm.url, vm.contents)

    return HTTPFound('/admin/pages')


#################################################
#       ADD REDIRECT
#
@view_config(route_name='add_redirect',
             request_method='GET',
             renderer='pypi:templates/admin/edit_redirect.pt')
@permissions.admin
def add_redirect_get(request: Request):
    vm = EditRedirectViewModel(request)
    return vm.to_dict()


@view_config(route_name='add_redirect',
             request_method='POST',
             renderer='pypi:templates/admin/edit_redirect.pt')
@permissions.admin
def add_redirect_post(request: Request):
    return add_or_edit_redirect(request)


#################################################
#       EDIT REDIRECT
#
@view_config(route_name='edit_redirect',
             request_method='GET',
             renderer='pypi:templates/admin/edit_redirect.pt')
@permissions.admin
def edit_redirect_get(request: Request):
    vm = EditRedirectViewModel(request)
    return vm.to_dict()


@view_config(route_name='edit_redirect',
             request_method='POST',
             renderer='pypi:templates/admin/edit_redirect.pt')
@permissions.admin
def edit_redirect_post(request: Request):
    return add_or_edit_redirect(request)


def add_or_edit_redirect(request: Request):
    vm = EditRedirectViewModel(request)

    vm.process_form()
    if vm.error:
        return vm.to_dict()

    if vm.redirect_id:
        cms_service.update_redirect(vm.redirect_id, vm.name, vm.short_url, vm.url)
    else:
        cms_service.create_redirect(vm.name, vm.short_url, vm.url)

    return HTTPFound('/admin/redirects')
