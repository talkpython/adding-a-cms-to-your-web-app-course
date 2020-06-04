import flask
import markdown_subtemplate

from pypi_org.services import cms_service
from pypi_org.viewmodels.shared.viewmodelbase import ViewModelBase


class RequestViewModel(ViewModelBase):
    def __init__(self, url):
        super().__init__()

        self.url = url
        self.page = cms_service.get_page(self.url)
        self.html = None
        if self.page:
            self.html = markdown_subtemplate.engine.get_page(url)
            # self.html = self.convert_to_markdown(   self.page.contents)
            # self.html = self.convert_to_markdown((self.page.contents+'\n')*20)

        self.redirect = cms_service.get_redirect(self.url)
        self.redirect_url = None
        if self.redirect:
            dest = self.redirect.url
            query = flask.request.query_string
            if query:
                query = query.decode('utf-8')
                dest = f'{dest}?{query}'
            self.redirect_url = dest

    # noinspection PyMethodMayBeStatic
    # def convert_to_markdown(self, md_text) -> str:
    #     options = [
    #         "cuddled-lists",
    #         "code-friendly",
    #         "fenced-code-blocks",
    #         "tables",
    #     ]
    #
    #     html = markdown2.markdown(md_text, extras=options, safe_mode=True)
    #     return html
