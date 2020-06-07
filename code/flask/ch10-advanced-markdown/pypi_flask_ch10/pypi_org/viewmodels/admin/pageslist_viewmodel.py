from pypi_org.services import cms_service
from pypi_org.viewmodels.shared.viewmodelbase import ViewModelBase


class PagesListViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()

        all_pages = cms_service.all_pages()

        self.pages = [p for p in all_pages if not p.is_shared]
        self.shared = [p for p in all_pages if p.is_shared]
