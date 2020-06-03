from pypi_org.services import cms_service
from pypi_org.viewmodels.shared.viewmodelbase import ViewModelBase


class EditPageViewModel(ViewModelBase):
    def __init__(self, page_id: int = 0):
        super().__init__()

        self.page_id = page_id
        self.page = None
        self.title = ''
        self.url = ''
        self.contents = ''

        if self.page_id:
            self.page = cms_service.get_page_by_id(self.page_id)

        if self.page:
            self.title = self.page.title
            self.url = self.page.url
            self.contents = self.page.contents

    def process_form(self):
        d = self.request_dict
        self.title = d.get('title', '').strip()
        self.url = d.get('url', '').strip().lower()
        self.contents = d.get('contents', '').strip()

    def validate(self) -> bool:
        if not self.title or not self.title.strip():
            self.error = 'You must specify a title.'
            return False

        if not self.url or not self.url.strip():
            self.error = 'You must specify a url.'
            return False

        if self.page_id and not self.page:
            self.error = f"The page with ID {self.page_id} doesn't exist."
            return False

        if not self.page_id and cms_service.get_page(self.url):
            self.error = f"The page with url /{self.url} already exists."
            return False

        return True
