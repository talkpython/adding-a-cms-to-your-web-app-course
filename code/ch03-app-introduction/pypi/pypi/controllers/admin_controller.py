import pyramid.httpexceptions as x
from pyramid.request import Request
from pyramid.view import view_config

from pypi.services import cms_service
from pypi.viewmodels.admin.admin_home_viewmodel import AdminHomeViewModel
from pypi.viewmodels.admin.edit_cmspage_viewmodel import EditCmsPageViewModel
from pypi.viewmodels.admin.edit_redirect_viewmodel import EditRedirectViewModel
# ################### INDEX #################################
#
from pypi.viewmodels.admin.pages_viewmodel import PagesViewModel
from pypi.viewmodels.admin.redirects_viewmodel import RedirectsViewModel


@view_config(route_name='admin_home',
             renderer='pypi:templates/admin/index.pt')
def index(request):
    vm = AdminHomeViewModel(request)
    error_resp = valid_admin(vm.user)
    if error_resp:
        return error_resp

    return vm.to_dict()


# ################### REDIRECTS #################################
#
@view_config(route_name='redirects',
             renderer='pypi:templates/admin/redirects.pt')
def redirects(request):
    vm = RedirectsViewModel(request)
    error_resp = valid_admin(vm.user)
    if error_resp:
        return error_resp

    return vm.to_dict()


# ################### ADD_REDIRECT #################################

@view_config(route_name='add_redirect',
             renderer='pypi:templates/admin/edit_redirect.pt',
             request_method='GET')
def add_redirect_get(request):
    return add_or_edit_get(request)


@view_config(route_name='add_redirect',
             renderer='pypi:templates/account/edit_redirect.pt',
             request_method='POST')
def add_redirect_post(request: Request):
    return add_or_edit_post(request)


# ################### EDIT_REDIRECT #################################

@view_config(route_name='edit_redirect',
             renderer='pypi:templates/admin/edit_redirect.pt',
             request_method='GET')
def edit_redirect_get(request):
    return add_or_edit_get(request)


@view_config(route_name='edit_redirect',
             renderer='pypi:templates/account/edit_redirect.pt',
             request_method='POST')
def edit_redirect_post(request: Request):
    return add_or_edit_post(request)


# ################### PAGES #################################
#
@view_config(route_name='pages',
             renderer='pypi:templates/admin/pages.pt')
def pages(request):
    vm = PagesViewModel(request)
    error_resp = valid_admin(vm.user)
    if error_resp:
        return error_resp

    return vm.to_dict()


# ################### ADD_PAGE #################################

@view_config(route_name='add_page',
             renderer='pypi:templates/admin/edit_page.pt',
             request_method='GET')
def add_page_get(request):
    return add_or_edit_page_get(request)


@view_config(route_name='add_page',
             renderer='pypi:templates/account/edit_page.pt',
             request_method='POST')
def add_page_post(request: Request):
    return add_or_edit_page_post(request)


# ################### EDIT_PAGE #################################

@view_config(route_name='edit_page',
             renderer='pypi:templates/admin/edit_page.pt',
             request_method='GET')
def edit_redirect_get(request):
    return add_or_edit_page_get(request)


@view_config(route_name='edit_page',
             renderer='pypi:templates/account/edit_page.pt',
             request_method='POST')
def edit_redirect_post(request: Request):
    return add_or_edit_page_post(request)


# ################### REDIRECT HELPERS #############################

def add_or_edit_get(request: Request):
    vm = EditRedirectViewModel(request)
    error_resp = valid_admin(vm.user)
    if error_resp:
        return error_resp

    return vm.to_dict()


def add_or_edit_post(request: Request):
    vm = EditRedirectViewModel(request)
    vm.restore_from_dict()

    error_resp = valid_admin(vm.user)
    if error_resp:
        return error_resp

    if vm.error:
        return vm.to_dict()

    # create redirect
    redirect = cms_service.upsert_redirect(vm.redirect_id, vm.name, vm.short_url, vm.url)
    print(f"{vm.user.name} created/modified redirect: {redirect.short_url} -> {redirect.url}")

    return x.HTTPFound('/admin/redirects')


# ################### PAGE HELPERS #############################

def add_or_edit_page_get(request: Request):
    vm = EditCmsPageViewModel(request)
    error_resp = valid_admin(vm.user)
    if error_resp:
        return error_resp

    return vm.to_dict()


def add_or_edit_page_post(request: Request):
    vm = EditCmsPageViewModel(request)
    vm.restore_from_dict()

    error_resp = valid_admin(vm.user)
    if error_resp:
        return error_resp

    if vm.error:
        return vm.to_dict()

    # create page
    page = cms_service.upsert_page(vm.page_id, vm.title, vm.url, vm.contents)
    print(f"{vm.user.name} created/modified cms page: {page.title} -> {page.url}")

    return x.HTTPFound('/admin/pages')


def valid_admin(user):
    if not user:
        return x.HTTPFound('/account/login')

    if not user.is_admin:
        return x.HTTPForbidden()

    return None
