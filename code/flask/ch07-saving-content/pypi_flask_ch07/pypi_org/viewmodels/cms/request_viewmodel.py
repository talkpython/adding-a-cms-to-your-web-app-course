import flask

from pypi_org.services import cms_service
from pypi_org.viewmodels.shared.viewmodelbase import ViewModelBase


class RequestViewModel(ViewModelBase):
    def __init__(self, url):
        super().__init__()

        self.url = url
        self.page = cms_service.get_page(self.url)
        self.html = None
        if self.page:
            self.html = self.page.contents

        self.redirect = cms_service.get_redirect(self.url)
        self.redirect_url = None
        if self.redirect:
            dest = self.redirect.url
            query = flask.request.query_string
            if query:
                query = query.decode('utf-8')
                dest = f'{dest}?{query}'
            self.redirect_url = dest
