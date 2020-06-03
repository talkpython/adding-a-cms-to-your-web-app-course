import flask

from pypi_org.infrastructure.view_modifiers import response
from pypi_org.viewmodels.cms.request_viewmodel import RequestViewModel

blueprint = flask.Blueprint('cms', __name__, template_folder='templates')


@blueprint.route('/<path:full_url>')
@response(template_file='cms/page.html')
def cms_request(full_url):
    vm = RequestViewModel(full_url)

    if vm.page:
        return vm.to_dict()

    if vm.redirect:
        return flask.redirect(vm.redirect_url)

    return flask.abort(404)
