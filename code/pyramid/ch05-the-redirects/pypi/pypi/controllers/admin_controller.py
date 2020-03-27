from pyramid.httpexceptions import HTTPFound
from pyramid.request import Request
from pyramid.view import view_config

from pypi.infrastructure import permissions
from pypi.services import cms_service
from pypi.viewmodels.admin.editredirect_viewmodel import EditRedirectViewModel
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

    if vm.redirect:
        cms_service.update_redirect(vm.redirect_id, vm.name, vm.short_url, vm.url)
    else:
        cms_service.create_redirect(vm.name, vm.short_url, vm.url)

    return HTTPFound('/admin/redirects')
