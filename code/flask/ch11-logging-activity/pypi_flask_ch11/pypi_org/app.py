import os
import sys

from markdown_subtemplate import storage, logging

from pypi_org.infrastructure.log_levels import LogLevel
from pypi_org.infrastructure.template_log_engine import TemplateLogger
from pypi_org.infrastructure.template_storage_engine import TemplateDBStorage

# region Additional imports after updating project path.

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, folder)

import logbook
import flask
import pypi_org.data.db_session as db_session

# endregion

app = flask.Flask(__name__)


def main():
    log = configure()
    debug = True
    port = 5006
    log.notice(f"Starting app: localhost:{port}, debug: {debug}")
    app.run(debug=debug, host="localhost", port=port)


def configure():
    log = init_logging()
    log.notice("Configuring Flask app:")
    register_blueprints(log)
    setup_db(log)
    setup_markdown(log)

    return log


def init_logging():
    logbook.StreamHandler(sys.stdout, level=LogLevel.info).push_application()
    return logbook.Logger('App')


def setup_markdown(log: logbook.Logger):
    store = TemplateDBStorage()
    storage.set_storage(store)

    log_engine = TemplateLogger(logging.LogLevel.info)
    logging.set_log(log_engine)
    log.notice(f"Set markdown storage engine to: {type(store).__name__}.")
    log.notice(f"Set markdown log engine to: {type(log_engine).__name__}.")


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
    from pypi_org.views import account_views
    from pypi_org.views import seo_view
    from pypi_org.views import cms_views
    from pypi_org.views import error_views
    from pypi_org.views import admin_views

    app.register_blueprint(home_views.blueprint)
    app.register_blueprint(error_views.blueprint)
    app.register_blueprint(package_views.blueprint)
    app.register_blueprint(account_views.blueprint)
    app.register_blueprint(seo_view.blueprint)
    app.register_blueprint(admin_views.blueprint)
    app.register_blueprint(cms_views.blueprint)

    log.notice("Registered blueprints.")


if __name__ == '__main__':
    main()
else:
    configure()
