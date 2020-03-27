import markdown_subtemplate
from pypi_org.services import cms_service
from pypi_org.viewmodels.shared.viewmodelbase import ViewModelBase


class CMSRequestViewModel(ViewModelBase):
    def __init__(self, full_url: str):
        super().__init__()

        self.full_url = full_url

        self.redirect = cms_service.get_redirect(self.full_url)
        self.page = cms_service.get_page(self.full_url)
        self.html = ''

        if self.page:
            self.html = markdown_subtemplate.engine.get_page(self.full_url)
            if self.html is None:
                self.html = f"[ERROR: MISSING CONTENT FOR {self.full_url}]"

    @property
    def redirect_url(self):
        query = self.request.query_string
        url = self.redirect.url
        if query:
            url = f'{url}?{query}'

        return url
