import os
import sys

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, folder)

from markdown_subtemplate.logging import LogLevel
from markdown_subtemplate import storage, logging
import logbook
import flask
import pypi_org.data.db_session as db_session
from pypi_org.infrastructure.template_storage_engine import SubTemplateDBStorage
from pypi_org.infrastructure.template_log_engine import SubTemplateLogger

app = flask.Flask(__name__)


def main():
    log = configure()
    debug = True
    port = 5006
    log.notice(f"Starting app: localhost:{port} , debug: {debug}")
    app.run(debug=debug, port=port)


def configure():
    log = init_logging()
    log.notice("Configuring Flask app:")
    register_blueprints(log)
    init_markdown(log)
    setup_db(log)

    return log


def init_logging():
    logbook.StreamHandler(sys.stdout).push_application()
    return logbook.Logger('App')


def init_markdown(log: logbook.Logger):
    log_engine = SubTemplateLogger(LogLevel.trace)
    logging.set_log(log_engine)

    store = SubTemplateDBStorage()
    storage.set_storage(store)

    log.notice(
        f"Registered markdown storage engine: {type(store).__qualname__}")
    log.notice(
        f"Registered markdown logging engine: {type(log_engine).__qualname__}")


def setup_db(log: logbook.Logger):
    db_file = os.path.join(
        os.path.dirname(__file__),
        'db',
        'pypi.sqlite')

    db_session.global_init(db_file)
    log.notice(f'Database initialized.')


def register_blueprints(log: logbook.Logger):
    from pypi_org.views import home_views
    from pypi_org.views import package_views
    from pypi_org.views import cms_views
    from pypi_org.views import account_views
    from pypi_org.views import seo_view
    from pypi_org.views import admin_views

    app.register_blueprint(package_views.blueprint)
    app.register_blueprint(home_views.blueprint)
    app.register_blueprint(account_views.blueprint)
    app.register_blueprint(seo_view.blueprint)
    app.register_blueprint(cms_views.blueprint)
    app.register_blueprint(admin_views.blueprint)

    log.notice("Registered blueprints.")


if __name__ == '__main__':
    main()
else:
    configure()
