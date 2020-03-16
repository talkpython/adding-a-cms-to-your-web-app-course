from pyramid.httpexceptions import HTTPForbidden
from pyramid.request import Request
from pyramid.view import view_config

from pypi.data.users import User
from pypi.viewmodels.shared.viewmodel_base import ViewModelBase


@view_config(route_name='admin_index', renderer='pypi:templates/admin/index.pt')
def index(request: Request):
    vm = ViewModelBase(request)
    validate_is_admin(vm.user)

    return vm.to_dict()


def validate_is_admin(user: User):
    if not user or not user.is_admin:
        raise HTTPForbidden("You don't have access to this section of the site.")
