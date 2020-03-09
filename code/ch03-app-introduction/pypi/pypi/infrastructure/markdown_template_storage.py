from typing import Optional

from markdown_subtemplate import storage
from markdown_subtemplate.exceptions import ArgumentExpectedException

from pypi import DbSession
from pypi.data.markdown_page import MarkdownPage


class MarkdownSubTemplateDBStorage(storage.SubtemplateStorage):
    def get_markdown_text(self, template_path: str) -> Optional[str]:
        if not template_path:
            return None

        template_path = template_path.strip().lower()
        session = DbSession.create()

        mk: MarkdownPage = session.query(MarkdownPage) \
            .filter(MarkdownPage.id == template_path) \
            .first()

        session.close()

        if not mk:
            return None

        return mk.text

    # noinspection PyMethodMayBeStatic
    def save_markdown_text(self, template_path: str, markdown_text: str):
        if not template_path:
            raise ArgumentExpectedException('template_path')

        template_path = template_path.strip().lower()
        session = DbSession.create()

        mk: MarkdownPage = session.query(MarkdownPage) \
            .filter(MarkdownPage.id == template_path) \
            .first()

        if not mk:
            mk = MarkdownPage()
            mk.id = template_path
            mk.name = template_path
            session.add(mk)

        mk.text = markdown_text

        session.commit()
        session.close()

    def get_shared_markdown(self, import_name: str) -> Optional[str]:
        if not import_name:
            return None

        import_name = import_name.strip().lower()
        session = DbSession.create()

        mk: MarkdownPage = session.query(MarkdownPage) \
            .filter(MarkdownPage.name == import_name, MarkdownPage.is_shared == True) \
            .first()

        session.close()

        if not mk:
            return None

        return mk.text

    def is_initialized(self) -> bool:
        return DbSession.is_initialized

    def clear_settings(self):
        raise NotImplemented('clear_settings')
