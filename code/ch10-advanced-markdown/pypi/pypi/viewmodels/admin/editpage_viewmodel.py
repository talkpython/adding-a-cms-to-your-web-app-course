from pyramid.request import Request

from pypi.services import cms_service
from pypi.viewmodels.shared.viewmodel_base import ViewModelBase


class EditPageViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.url = ''
        self.title = ''
        self.contents = ''
        self.is_shared = False
        self.page_id = int(self.request_dict.get('page_id', 0))
        self.page = cms_service.get_page_by_id(self.page_id)
        self.error = None

        if self.page:
            self.url = self.page.url
            self.title = self.page.title
            self.contents = self.page.contents
            self.is_shared = self.page.is_shared

    def process_form(self):
        d = self.request_dict
        self.url = d.get('url')
        self.contents = d.get('contents')
        self.is_shared = d.get('is_shared') == 'on'
        self.title = d.get('title')
        self.page_id = int(d.get('page_id', 0))

        if not self.url:
            self.error = "You must specify a url"

        if not self.page and cms_service.get_page(self.url):
            self.error = f"A page with url {self.url} already exists!"
        if self.page and not cms_service.get_page_by_id(self.page_id):
            self.error = f"A page with ID {self.page_id} was not found!"
