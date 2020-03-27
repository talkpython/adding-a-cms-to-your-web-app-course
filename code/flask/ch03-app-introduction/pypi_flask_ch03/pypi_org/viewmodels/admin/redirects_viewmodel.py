from typing import List

from pypi_org.data.redirects import Redirect
from pypi_org.services import cms_service
from pypi_org.viewmodels.shared.viewmodelbase import ViewModelBase


class RedirectsViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.redirects: List[Redirect] = cms_service.all_redirects()
