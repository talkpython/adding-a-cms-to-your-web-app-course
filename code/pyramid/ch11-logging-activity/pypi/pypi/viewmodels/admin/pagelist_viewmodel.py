from pyramid.request import Request

from pypi.services import cms_service
from pypi.viewmodels.shared.viewmodel_base import ViewModelBase


class PagesListViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        pages = cms_service.all_pages()

        self.pages = [p for p in pages if not p.is_shared]
        self.subpages = [p for p in pages if p.is_shared]
