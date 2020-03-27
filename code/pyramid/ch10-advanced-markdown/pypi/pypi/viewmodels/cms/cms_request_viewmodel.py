from pyramid.request import Request
import markdown_subtemplate

from pypi.services import cms_service
from pypi.viewmodels.shared.viewmodel_base import ViewModelBase


class CmsRequestViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.sub_path = request.matchdict.get('sub_path')
        self.url = '/'.join(self.sub_path)

        self.page = cms_service.get_page(self.url)
        self.html = None
        if self.page:
            self.html = markdown_subtemplate.engine.get_page(self.url)
            # self.html = self.convert_to_markdown(self.page.contents)
            # self.html = self.convert_to_markdown((self.page.contents + '\n')*20)

        self.redirect = cms_service.get_redirect(self.url)
        self.redirect_url = None
        if self.redirect:
            self.redirect_url = self.redirect.url
            if request.query_string:
                self.redirect_url = f'{self.redirect_url}?{request.query_string}'

    # noinspection PyMethodMayBeStatic
    # def convert_to_markdown(self, md_text) -> str:
    #     extras = [
    #         "cuddled-lists",
    #         "code-friendly",
    #         "fenced-code-blocks",
    #         "tables"
    #     ]
    #
    #     html = markdown2.markdown(md_text, extras=extras, safe_mode=True)
    #     return html
