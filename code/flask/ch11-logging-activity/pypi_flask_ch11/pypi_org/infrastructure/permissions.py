from functools import wraps

import flask
import logbook

from pypi_org.viewmodels.shared.viewmodelbase import ViewModelBase

log = logbook.Logger("Permissions")


def admin(view_function):
    @wraps(view_function)
    def checker_function(*args, **kwargs):
        vm = ViewModelBase()
        if not vm.user:
            log.notice(f"Anonymous user attempting to access admin action, BLOCKED.")
            return flask.abort(status=403)

        if not vm.user.is_admin:
            log.notice(f"Non-admin user attempting to access admin action: {vm.user.email}, BLOCKED.")
            return flask.abort(status=403)

        log.trace(f"User permitted admin action: {vm.user.email}")
        return view_function(*args, **kwargs)

    return checker_function
