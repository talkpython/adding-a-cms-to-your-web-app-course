import os
import sys

import logbook
from markdown_subtemplate import storage, logging
from markdown_subtemplate.logging import LogLevel
from pyramid.config import Configurator

from pypi.data.db_session import DbSession
from pypi.infrastructure.template_storage_engine import SubTemplateDBStorage


def main(_, **settings):
    config = Configurator(settings=settings)
    log = init_logging(config)
    init_includes(config)
    init_db(log)
    init_markdown(log)
    init_routing(config, log)

    return config.make_wsgi_app()


def init_logging(config) -> logbook.Logger:
    logbook.StreamHandler(sys.stdout, level='NOTICE').push_application()
    log = logbook.Logger('App')
    log.notice('Logging initialized.')

    md_log = logging.get_log()
    md_log.log_level = LogLevel.info

    return log


def init_markdown(log: logbook.Logger):
    store = SubTemplateDBStorage()
    storage.set_storage(store)

    log.notice(f'Markdown storage engine set: {type(store).__name__}.')


def init_includes(config):
    config.include('pyramid_chameleon')


def init_routing(config, log: logbook.Logger):
    config.add_static_view('static', 'static', cache_max_age=3600)

    # home controller
    config.add_route('home', '/')
    config.add_route('about', '/about')

    # package controller
    config.add_route('popular', '/{num}', custom_predicates=[
        lambda info, _: info['match'].get('num', '').isdigit()
    ])

    config.add_route('package_details', '/project/{package_name}')
    config.add_route('package_details/', '/project/{package_name}/')

    config.add_route('releases', '/project/{package_name}/releases')
    config.add_route('releases/', '/project/{package_name}/releases/')

    config.add_route('release_version', '/project/{package_name}/releases/{release_version}')

    # account controller
    config.add_route('account_home', '/account')
    config.add_route('login', '/account/login')
    config.add_route('register', '/account/register')
    config.add_route('logout', '/account/logout')

    # utils controller
    config.add_route('sitemap.xml', '/sitemap.xml')
    config.add_route('robots.txt', '/robots.txt')

    # admin controller
    config.add_route('admin_index', '/admin')
    config.add_route('redirects', '/admin/redirects')
    config.add_route('add_redirect', '/admin/add_redirect')
    config.add_route('edit_redirect', '/admin/edit_redirect/{redirect_id}')

    config.add_route('pages', '/admin/pages')
    config.add_route('add_page', '/admin/add_page')
    config.add_route('edit_page', '/admin/edit_page/{page_id}')

    # CMS Route
    # /company/history
    # sub_path = [company, history]
    config.add_route('cms_request', '*sub_path')

    config.scan()

    routes = config.get_routes_mapper().get_routes(True)
    log.notice(f'Web routes registered: {len(routes)} routes.')


def init_db(log: logbook.Logger):
    db_file = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            'db',
            'pypi.sqlite'
        ))
    DbSession.global_init(db_file)

    log.notice('DB initialized.')
