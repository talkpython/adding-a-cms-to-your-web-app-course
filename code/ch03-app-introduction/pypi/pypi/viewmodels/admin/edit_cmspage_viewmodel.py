from typing import Optional

from pyramid.request import Request

from pypi.data.pages import Page
from pypi.services import cms_service, user_service
from pypi.viewmodels.shared.viewmodel_base import ViewModelBase


class EditCmsPageViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.title = ''
        self.url = ''
        self.contents: str = ''
        self.page_id: Optional[int] = int(self.request_dict.get('page_id', 0))
        self.page: Optional[Page] = None

        if self.page_id:
            self.page = cms_service.get_page_by_id(self.page_id)
            if not self.page:
                self.error = f"A CMS page with id {self.page_id} does not exists."
                return

            self.title = self.page.title
            self.url = self.page.url
            self.contents = self.page.contents
            if self.contents:
                self.contents = self.contents.strip()

    def restore_from_dict(self):
        self.title = self.request_dict.get('title', self.title)
        self.url = self.request_dict.get('url', self.url)
        self.contents = self.request_dict.get('contents')
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
