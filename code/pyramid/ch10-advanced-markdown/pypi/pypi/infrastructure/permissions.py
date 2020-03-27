from pyramid.httpexceptions import HTTPForbidden
from pyramid.request import Request

from pypi.viewmodels.shared.viewmodel_base import ViewModelBase


def admin(view_function):
    def checker_function(request: Request):
        vm = ViewModelBase(request)
        if not vm.user or not vm.user.is_admin:
            raise HTTPForbidden('You must be an admin to access this section.')

        return view_function(request)

    return checker_function
