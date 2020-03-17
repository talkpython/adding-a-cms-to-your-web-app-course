from pyramid.request import Request
from pyramid.response import Response

from pypi.services import user_service, package_service, cms_service
from pypi.viewmodels.shared.viewmodel_base import ViewModelBase


class EditPageViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.url = ''
        self.title = ''
        self.contents = ''
        self.page_id = self.request_dict.get('page_id')
        self.page = cms_service.get_page_by_id(self.page_id)
        self.error = None

        if self.page:
            self.url = self.page.get('url')
            self.title = self.page.get('title')
            self.contents = self.page.get('contents')

    def process_form(self):
        d = self.request_dict
        self.url = d.get('url')
        self.contents = d.get('contents')
        self.title = d.get('title')
        self.page_id = d.get('page_id')

        if not self.url:
            self.error = "You must specify a url"

        if not self.page and cms_service.get_page(self.url):
            self.error = f"A page with url {self.url} already exists!"
        if self.page and not cms_service.get_redirect_by_id(self.page_id):
            self.error = f"A page with ID {self.page_id} was not found!"
