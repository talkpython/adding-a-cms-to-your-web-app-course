from typing import Optional

from markdown_subtemplate import storage

from pypi_org.data import db_session
from pypi_org.services import cms_service


class TemplateDBStorage(storage.SubtemplateStorage):
    def get_markdown_text(self, template_path) -> Optional[str]:
        page = cms_service.get_page(template_path, is_shared=False)
        if not page:
            return None

        return page.contents

    def get_shared_markdown(self, import_name) -> Optional[str]:
        page = cms_service.get_page(import_name, is_shared=True)
        if not page:
            return None

        return page.contents

    def is_initialized(self) -> bool:
        return db_session.is_initialized

    def clear_settings(self):
        pass
