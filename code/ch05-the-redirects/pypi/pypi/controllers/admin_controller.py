from pyramid.httpexceptions import HTTPForbidden
from pyramid.request import Request
from pyramid.view import view_config

from pypi.data.users import User
from pypi.infrastructure import permissions
from pypi.viewmodels.shared.viewmodel_base import ViewModelBase


@view_config(route_name='admin_index', renderer='pypi:templates/admin/index.pt')
@permissions.admin
def index(request: Request):
    vm = ViewModelBase(request)

    return vm.to_dict()
