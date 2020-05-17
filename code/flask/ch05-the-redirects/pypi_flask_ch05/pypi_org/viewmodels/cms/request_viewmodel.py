import flask

from pypi_org.services import cms_service
from pypi_org.viewmodels.shared.viewmodelbase import ViewModelBase


class RequestViewModel(ViewModelBase):
    def __init__(self, url):
        super().__init__()

        self.url = url

    @property
    def page(self):
        page = cms_service.get_page(self.url)
        return page

    @property
    def redirect(self):
        redir = cms_service.get_redirect(self.url)
        return redir

    @property
    def redirect_url(self):
        redirect = self.redirect
        if redirect:
            dest = redirect.get('url')
            query = flask.request.query_string
            if query:
                query = query.decode('utf-8')
                dest = f'{dest}?{query}'

        return dest
