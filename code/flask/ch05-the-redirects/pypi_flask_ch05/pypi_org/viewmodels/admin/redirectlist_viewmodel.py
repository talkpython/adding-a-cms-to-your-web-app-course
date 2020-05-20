from pypi_org.services import cms_service
from pypi_org.viewmodels.shared.viewmodelbase import ViewModelBase


class RedirectListViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()

        self.redirects = cms_service.all_redirects()
