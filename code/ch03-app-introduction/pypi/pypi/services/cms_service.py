from typing import Optional, List

from markdown_subtemplate import storage, caching

from pypi import DbSession, MarkdownSubTemplateDBStorage
from pypi.data.pages import Page
from pypi.data.redirects import Redirect


def get_redirect(short_url: str) -> Optional[Redirect]:
    if not short_url or not short_url.strip():
        return None

    short_url = short_url.strip().lower()

    session = DbSession.create()
    redirect = session.query(Redirect).filter(Redirect.short_url == short_url).first()
    session.close()

    return redirect


def upsert_redirect(rid: Optional[int], name: str, short_url: str, url: str) -> Optional[Redirect]:
    if not url or not url.strip() or not short_url or not short_url.strip():
        return None

    url = url.strip().lower()
    short_url = short_url.strip().lower()

    session = DbSession.create()
    redirect = session.query(Redirect).filter(Redirect.id == rid).first()
    if not redirect:
        redirect = Redirect()
        session.add(redirect)

    redirect.name = name
    redirect.url = url
    redirect.short_url = short_url

    session.commit()
    session.close()

    return redirect


def upsert_page(page_id: Optional[int], title: str, url: str, contents: str) -> Optional[Page]:
    if not url or not url.strip() or not title or not title.strip():
        return None

    url = url.strip().lower().strip('/')
    title = title.strip()
    if contents:
        contents = contents.strip()

    session = DbSession.create()
    page = session.query(Page).filter(Page.id == page_id).first()
    if not page:
        page = Page()
        session.add(page)

    page.title = title
    page.url = url
    page.contents = contents

    session.commit()
    session.close()

    add_page_to_markdown_storage(page)

    return page


def add_page_to_markdown_storage(page: Page):
    # noinspection PyTypeChecker
    store: MarkdownSubTemplateDBStorage = storage.get_storage()
    store.save_markdown_text(page.url, page.contents)
    caching.get_cache().clear()


def get_page(url: str):
    if not url or not url.strip():
        return None

    session = DbSession.create()
    url = url.strip().lower()

    page = session.query(Page).filter(Page.url == url).first()

    session.close()

    return page


def all_redirects() -> List[Redirect]:
    session = DbSession.create()
    redirects = session.query(Redirect).order_by(Redirect.created_date.desc()).all()
    session.close()
    return redirects


def all_pages() -> List[Page]:
    session = DbSession.create()
    pages = session.query(Page).order_by(Page.created_date.desc()).all()
    session.close()
    return pages


def get_redirect_by_id(redirect_id: int) -> Optional[Redirect]:
    session = DbSession.create()
    redirect = session.query(Redirect).filter(Redirect.id == redirect_id).first()

    session.close()
    return redirect


def get_page_by_id(page_id: int) -> Optional[Page]:
    session = DbSession.create()
    page = session.query(Page).filter(Page.id == page_id).first()

    session.close()
    return page
