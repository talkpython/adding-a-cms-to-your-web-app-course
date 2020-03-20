from pyramid.request import Request

from pypi.services import cms_service
from pypi.viewmodels.shared.viewmodel_base import ViewModelBase


class PagesListViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.pages = cms_service.all_pages()
