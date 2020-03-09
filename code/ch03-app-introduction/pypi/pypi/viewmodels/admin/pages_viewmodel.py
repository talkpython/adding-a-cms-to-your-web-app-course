from typing import List, Optional

from pyramid.request import Request

from pypi.data.pages import Page
from pypi.data.users import User
from pypi.services import cms_service, user_service
from pypi.viewmodels.shared.viewmodel_base import ViewModelBase


class PagesViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)
        self.pages: List[Page] = cms_service.all_pages()
