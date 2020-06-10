import flask
import logbook

from pypi_org.infrastructure.view_modifiers import response
from pypi_org.viewmodels.cms.request_viewmodel import RequestViewModel

blueprint = flask.Blueprint('cms', __name__, template_folder='templates')
log = logbook.Logger('CMS')


@blueprint.route('/<path:full_url>')
@response(template_file='cms/page.html')
def cms_request(full_url):
    vm = RequestViewModel(full_url)

    if vm.page:
        log.trace(f'CMS request for page: {vm.page.title}')
        return vm.to_dict()

    if vm.redirect:
        log.trace(f'CMS request for redirect: {vm.redirect.short_url}')
        return flask.redirect(vm.redirect_url)

    log.info(f'CMS request not found: {vm.url}')
    return flask.abort(404)
