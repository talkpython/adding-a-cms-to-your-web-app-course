from typing import Optional

from markdown_subtemplate import storage

from pypi import DbSession
from pypi.services import cms_service


class SubTemplateDBStorage(storage.SubtemplateStorage):
    def get_markdown_text(self, template_path) -> Optional[str]:
        page = cms_service.get_page(template_path)
        if not page:
            return None

        return page.contents

    def get_shared_markdown(self, import_name) -> Optional[str]:
        page = cms_service.get_page(import_name)
        if not page:
            return None

        return page.contents

    def is_initialized(self) -> bool:
        return DbSession.is_initialized

    def clear_settings(self):
        pass
