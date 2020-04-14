import flask

blueprint = flask.Blueprint('errors', __name__, template_folder='templates')


@blueprint.app_errorhandler(404)
def error_404(_):
    resp = flask.render_template('errors/404.html')
    return resp, 404
