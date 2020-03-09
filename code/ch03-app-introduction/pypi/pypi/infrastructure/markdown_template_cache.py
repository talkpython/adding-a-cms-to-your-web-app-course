from markdown_subtemplate import caching

from pypi import DbSession
from pypi.data.markdown_cache import MarkdownCache


class MarkdownSubTemplateDBCache(caching.SubtemplateCache):
    def get_html(self, key: str) -> caching.CacheEntry:
        session = DbSession.create()

        cache_entry = session.query(MarkdownCache).filter(
            MarkdownCache.key == key, MarkdownCache.type == 'html'
        ).first()

        session.close()

        return cache_entry

    def add_html(self, key: str, name: str, html_contents: str) -> caching.CacheEntry:
        session = DbSession.create()

        item = self.get_html(key)
        if not item:
            item = MarkdownCache()
            session.add(item)

        item.type = 'html'
        item.key = key
        item.name = name
        item.contents = html_contents

        if html_contents:
            session.commit()

        session.close()

        # Not technical a base class, but duck-type equivalent.
        # noinspection PyTypeChecker
        return item

    def get_markdown(self, key: str) -> caching.CacheEntry:
        session = DbSession.create()

        cache_entry = session.query(MarkdownCache).filter(
            MarkdownCache.key == key, MarkdownCache.type == 'markdown'
        ).first()

        session.close()

        return cache_entry

    def add_markdown(self, key: str, name: str, markdown_contents: str) -> caching.CacheEntry:
        session = DbSession.create()

        item = self.get_markdown(key)
        if not item:
            item = MarkdownCache()
            session.add(item)

        item.type = 'markdown'
        item.key = key
        item.name = name
        item.contents = markdown_contents

        if markdown_contents:
            session.commit()
        session.close()

        # Not technical a base class, but duck-type equivalent.
        # noinspection PyTypeChecker
        return item

    def clear(self):
        session = DbSession.create()

        for entry in session.query(MarkdownCache):
            session.delete(entry)

        session.commit()

    def count(self) -> int:
        session = DbSession.create()
        count = session.query(MarkdownCache).count()
        session.close()

        return count
