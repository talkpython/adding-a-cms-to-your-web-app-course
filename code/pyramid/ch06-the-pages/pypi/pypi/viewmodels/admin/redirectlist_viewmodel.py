from pyramid.request import Request
from pyramid.response import Response

from pypi.services import user_service, package_service, cms_service
from pypi.viewmodels.shared.viewmodel_base import ViewModelBase


class RedirectListViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.redirects = cms_service.all_redirects()
