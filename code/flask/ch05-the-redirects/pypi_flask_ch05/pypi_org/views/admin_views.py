import flask

from pypi_org.infrastructure import permissions
from pypi_org.infrastructure.view_modifiers import response
from pypi_org.services import cms_service
from pypi_org.viewmodels.admin.editredirect_viewmodel import EditRedirectViewModel
from pypi_org.viewmodels.admin.redirectlist_viewmodel import RedirectListViewModel
from pypi_org.viewmodels.shared.viewmodelbase import ViewModelBase

blueprint = flask.Blueprint('admin', __name__, template_folder='templates')


@permissions.admin
@blueprint.route('/admin')
@response(template_file='admin/index.html')
def index():
    vm = ViewModelBase()
    return vm.to_dict()


@permissions.admin
@blueprint.route('/admin/redirects')
@response(template_file='admin/redirects.html')
def redirects():
    vm = RedirectListViewModel()
    return vm.to_dict()


# ADD_REDIRECT VIEWS ####################################
#
#
@permissions.admin
@blueprint.route('/admin/add_redirect', methods=['GET'])
@response(template_file='admin/edit_redirect.html')
def add_redirect_get():
    vm = EditRedirectViewModel()
    return vm.to_dict()


@permissions.admin
@blueprint.route('/admin/add_redirect', methods=['POST'])
@response(template_file='admin/edit_redirect.html')
def add_redirect_post():
    vm = EditRedirectViewModel()
    vm.process_form()

    if not vm.validate():
        return vm.to_dict()

    cms_service.create_redirect(vm.name, vm.short_url, vm.url)

    return flask.redirect('/admin/redirects')


# EDIT_REDIRECT VIEWS ####################################
#
#
@permissions.admin
@blueprint.route('/admin/edit_redirect/<int:redirect_id>', methods=['GET'])
@response(template_file='admin/edit_redirect.html')
def edit_redirect_get(redirect_id: int):
    vm = EditRedirectViewModel(redirect_id)
    if not vm.redirect:
        return flask.abort(404)

    return vm.to_dict()


@permissions.admin
@blueprint.route('/admin/edit_redirect/<int:redirect_id>', methods=['POST'])
@response(template_file='admin/edit_redirect.html')
def edit_redirect_post(redirect_id: int):
    vm = EditRedirectViewModel(redirect_id)
    vm.process_form()

    if not vm.validate():
        return vm.to_dict()

    cms_service.update_redirect(vm.redirect_id, vm.name, vm.short_url, vm.url)

    return flask.redirect('/admin/redirects')
