import flask
import logbook

from pypi_org.infrastructure.view_modifiers import response
from pypi_org.viewmodels.cms.page_viewmodel import CMSRequestViewModel

blueprint = flask.Blueprint('cms', __name__, template_folder='templates')

log = logbook.Logger('CMS')


@blueprint.route('/<path:full_url>')
@response(template_file='cms/page.html')
def cms_request(full_url: str):
    vm = CMSRequestViewModel(full_url)
    if vm.page:
        log.trace(f'Processing CMS page request: {full_url}')
        return vm.to_dict()

    if vm.redirect:
        log.trace(f'Processing CMS redirect request: {full_url}')
        return flask.redirect(vm.redirect_url)

    log.trace(f'CMS entry not found (404): {full_url}')
    return flask.abort(status=404)
