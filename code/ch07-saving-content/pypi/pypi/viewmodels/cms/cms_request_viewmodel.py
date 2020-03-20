from pyramid.request import Request
from pyramid.response import Response

from pypi.services import user_service, package_service, cms_service
from pypi.viewmodels.shared.viewmodel_base import ViewModelBase


class CmsRequestViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.sub_path = request.matchdict.get('sub_path')
        self.url = '/'.join(self.sub_path)

        self.page = cms_service.get_page(self.url)
        self.html = None
        if self.page:
            self.html = self.page.get('contents')

        self.redirect = cms_service.get_redirect(self.url)
        self.redirect_url = None
        if self.redirect:
            self.redirect_url = self.redirect.url
            if request.query_string:
                self.redirect_url = f'{self.redirect_url}?{request.query_string}'
