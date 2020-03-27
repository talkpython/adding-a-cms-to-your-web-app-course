from typing import Optional

import flask
import logbook
from markdown_subtemplate import caching

from pypi_org.infrastructure import permissions
from pypi_org.infrastructure.view_modifiers import response
from pypi_org.services import cms_service
from pypi_org.viewmodels.admin.admin_home_viewmodel import AdminHomeViewModel
from pypi_org.viewmodels.admin.edit_cmspage_viewmodel import EditCmsPageViewModel
from pypi_org.viewmodels.admin.edit_redirect_viewmodel import EditRedirectViewModel
from pypi_org.viewmodels.admin.pages_viewmodel import PagesViewModel
from pypi_org.viewmodels.admin.redirects_viewmodel import RedirectsViewModel

blueprint = flask.Blueprint('admin', __name__, template_folder='templates')

log = logbook.Logger('Admin')


@permissions.admin
@blueprint.route('/admin')
@response(template_file='admin/index.html')
def index():
    vm = AdminHomeViewModel()
    return vm.to_dict()


@permissions.admin
@blueprint.route('/admin/redirects')
@response(template_file='admin/redirects.html')
def redirects():
    vm = RedirectsViewModel()
    return vm.to_dict()


@permissions.admin
@blueprint.route('/admin/pages')
@response(template_file='admin/pages.html')
def pages():
    vm = PagesViewModel()
    return vm.to_dict()


# ################### ADD_REDIRECT #################################

@permissions.admin
@blueprint.route('/admin/add_redirect', methods=['GET'])
@response(template_file='admin/edit_redirect.html')
def add_redirect_get():
    return add_or_edit_redirect_get()


@permissions.admin
@blueprint.route('/admin/add_redirect', methods=['POST'])
@response(template_file='admin/edit_redirect.html')
def add_redirect_post():
    return add_or_edit_redirect_post()


# ################### EDIT_REDIRECT #################################

@permissions.admin
@blueprint.route('/admin/edit_redirect/<redirect_id>', methods=['GET'])
@response(template_file='admin/edit_redirect.html')
def edit_redirect_get(redirect_id):
    return add_or_edit_redirect_get(redirect_id)


@permissions.admin
@blueprint.route('/admin/edit_redirect/<redirect_id>', methods=['POST'])
@response(template_file='admin/edit_redirect.html')
def edit_redirect_post(redirect_id):
    return add_or_edit_redirect_post(redirect_id)


# ################### ADD_PAGE #################################

@permissions.admin
@blueprint.route('/admin/add_page', methods=['GET'])
@response(template_file='admin/edit_page.html')
def add_page_get():
    return add_or_edit_page_get()


@permissions.admin
@blueprint.route('/admin/add_page', methods=['POST'])
@response(template_file='admin/edit_page.html')
def add_page_post():
    return add_or_edit_page_post()


# ################### EDIT_PAGE #################################

@permissions.admin
@blueprint.route('/admin/edit_page/<page_id>', methods=['GET'])
@response(template_file='admin/edit_page.html')
def edit_page_get(page_id):
    return add_or_edit_page_get(page_id)


@permissions.admin
@blueprint.route('/admin/edit_page/<page_id>', methods=['POST'])
@response(template_file='admin/edit_page.html')
def edit_page_post(page_id):
    return add_or_edit_page_post(page_id)


# ################### REDIRECT HELPERS #############################

def add_or_edit_redirect_get(redirect_id: Optional[str] = None):
    vm = EditRedirectViewModel(redirect_id)
    return vm.to_dict()


def add_or_edit_redirect_post(redirect_id: Optional[str] = None):
    vm = EditRedirectViewModel(redirect_id)
    vm.restore_from_dict()

    log.notice(f'{vm.user.name}')

    if vm.error:
        return vm.to_dict()

    # create redirect
    redirect = cms_service.upsert_redirect(vm.redirect_id, vm.name, vm.short_url, vm.url)
    print(f"{vm.user.name} created/modified redirect: {redirect.short_url} -> {redirect.url}")

    return flask.redirect('/admin/redirects')


# ################### PAGE HELPERS #############################

def add_or_edit_page_get(page_id: Optional[str] = None):
    vm = EditCmsPageViewModel(page_id)
    return vm.to_dict()


def add_or_edit_page_post(page_id: Optional[str] = None):
    vm = EditCmsPageViewModel(page_id)
    vm.restore_from_dict()

    if vm.error:
        return vm.to_dict()

    # create page
    page = cms_service.upsert_page(vm.page_id, vm.title, vm.url, vm.contents, vm.is_shared)
    caching.get_cache().clear()
    print(f"{vm.user.name} created/modified cms page: {page.title} -> {page.url}")

    return flask.redirect('/admin/pages')
