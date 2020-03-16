from pyramid.request import Request
from pyramid.response import Response

from pypi.services import user_service, package_service, cms_service
from pypi.viewmodels.shared.viewmodel_base import ViewModelBase


class EditRedirectViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.short_url = None
        self.url = None
        self.name = None
        self.redirect_id = None
        self.error = None

    def process_form(self):
        d = self.request_dict
        self.short_url = d.get('short_url')
        self.url = d.get('url')
        self.name = d.get('name')
        self.redirect_id = d.get('redirect_id')

        if not self.short_url:
            self.error = "You must specify a short url"

        if cms_service.get_redirect(self.short_url):
            self.error = f"A redirect with url {self.short_url} already exists!"
