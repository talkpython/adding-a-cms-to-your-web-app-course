import flask

blueprint = flask.Blueprint('cms', __name__, template_folder='templates')


@blueprint.route('/<path:full_url>')
def cms_request(full_url):
    # Check if the full_url matches some page or redirect
    return f"Hello CMS! You requested /{full_url}"
