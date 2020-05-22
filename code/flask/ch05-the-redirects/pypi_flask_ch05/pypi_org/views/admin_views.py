import flask

from pypi_org.infrastructure import permissions
from pypi_org.infrastructure.view_modifiers import response
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

    if not vm.validate():
        return vm.to_dict()

    print(f"WOULD HAVE CREATED: {vm.short_url} -> {vm.url}")
    return flask.redirect('/admin/redirects')
