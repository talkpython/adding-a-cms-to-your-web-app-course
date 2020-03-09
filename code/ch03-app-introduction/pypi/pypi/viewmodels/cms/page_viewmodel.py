from pyramid.request import Request
import markdown_subtemplate

from pypi.infrastructure import request_dict
from pypi.services import cms_service
from pypi.viewmodels.shared.viewmodel_base import ViewModelBase


class CMSRequestViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        data = request_dict.create(request)

        self.sub_path = data.get('sub_path')
        self.sub_url = None
        if self.sub_path:
            self.sub_url = '/'.join(self.sub_path)

        self.redirect = cms_service.get_redirect(self.sub_url)
        self.page = cms_service.get_page(self.sub_url)
        self.html = ''

        if self.page:
            template_path = self.sub_url
            self.html = markdown_subtemplate.engine.get_page(template_path)
            if self.html is None:
                self.html = f"[ERROR: MISSING CONTENT FOR {template_path}]"
