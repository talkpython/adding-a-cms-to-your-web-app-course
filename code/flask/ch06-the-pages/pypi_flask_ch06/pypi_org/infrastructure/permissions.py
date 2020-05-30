from functools import wraps

import flask

from pypi_org.viewmodels.shared.viewmodelbase import ViewModelBase


def admin(view_function):
    @wraps(view_function)
    def checker_function(*args, **kwargs):
        vm = ViewModelBase()
        if not vm.user or not vm.user.is_admin:
            return flask.abort(status=403)

        return view_function(*args, **kwargs)

    return checker_function
