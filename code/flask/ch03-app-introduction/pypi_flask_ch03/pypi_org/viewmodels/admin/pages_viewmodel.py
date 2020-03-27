from pypi_org.services import cms_service
from pypi_org.viewmodels.shared.viewmodelbase import ViewModelBase


class PagesViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        pages = cms_service.all_pages()

        self.pages = [p for p in pages if not p.is_shared]
        self.sub_pages = [p for p in pages if p.is_shared]
