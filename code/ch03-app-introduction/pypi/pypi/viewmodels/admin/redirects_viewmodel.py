from typing import List, Optional

from pyramid.request import Request

from pypi.data.redirects import Redirect
from pypi.data.users import User
from pypi.services import cms_service, user_service
from pypi.viewmodels.shared.viewmodel_base import ViewModelBase


class RedirectsViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)
        self.redirects: List[Redirect] = cms_service.all_redirects()
