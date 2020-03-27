from typing import Optional

from pypi_org.data.pages import Page
from pypi_org.infrastructure.num_convert import try_int
from pypi_org.services import cms_service
from pypi_org.viewmodels.shared.viewmodelbase import ViewModelBase


class EditCmsPageViewModel(ViewModelBase):
    def __init__(self, page_id: Optional[str] = None):
        super().__init__()

        self.title = ''
        self.url = ''
        self.contents: str = ''
        self.is_shared: bool = False
        self.page_id: Optional[int] = try_int(page_id)
        self.page: Optional[Page] = None

        if self.page_id:
            self.page = cms_service.get_page_by_id(self.page_id)
            if not self.page:
                self.error = f"A CMS page with id {self.page_id} does not exists."
                return

            self.title = self.page.title
            self.url = self.page.url
            self.contents = self.page.contents
            self.is_shared = self.page.is_shared
            if self.contents:
                self.contents = self.contents.strip()

    def restore_from_dict(self):
        d = self.request_dict
        self.title = d.get('title', self.title)
        self.url = d.get('url', self.url)
        self.contents = d.get('contents')
        self.is_shared = d.get('is_shared') == 'on'
        print(self.is_shared)
        if self.contents:
            self.contents = self.contents.strip()

        if not self.page_id:
            page = cms_service.get_page(self.url)
            if page:
                self.error = f"A CMS page with URL {self.url} already exists."
                return

        if not self.title or not self.title.strip():
            self.error = "A title is required."
            return

        if not self.url or not self.url.strip():
            self.error = "A url is required."
            return
