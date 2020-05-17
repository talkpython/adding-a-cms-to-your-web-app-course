import flask

from pypi_org.services import cms_service

blueprint = flask.Blueprint('cms', __name__, template_folder='templates')


@blueprint.route('/<path:full_url>')
def cms_request(full_url):
    page = cms_service.get_page(full_url)
    if page:
        return f"Title: {page.get('title')}, Contents: {page.get('contents')}"

    redirect = cms_service.get_redirect(full_url)
    if redirect:
        dest = redirect.get('url')
        query = flask.request.query_string
        if query:
            query = query.decode('utf-8')
            dest = f'{dest}?{query}'
        return flask.redirect(dest)

    return flask.abort(404)
