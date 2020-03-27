from typing import Optional, List

import pypi_org.data.db_session as db_session
from pypi_org.data.pages import Page
from pypi_org.data.redirects import Redirect


def get_redirect(short_url: str) -> Optional[Redirect]:
    if not short_url or not short_url.strip():
        return None

    short_url = short_url.strip().lower()

    session = db_session.create_session()
    try:
        return session.query(Redirect).filter(Redirect.short_url == short_url).first()
    finally:
        session.close()


def upsert_redirect(rid: Optional[int], name: str, short_url: str, url: str) -> Optional[Redirect]:
    if not url or not url.strip() or not short_url or not short_url.strip():
        return None

    url = url.strip().lower()
    short_url = short_url.strip().lower()

    session = db_session.create_session()
    try:
        redirect = session.query(Redirect).filter(Redirect.id == rid).first()
        if not redirect:
            redirect = Redirect()
            session.add(redirect)

        redirect.name = name
        redirect.url = url
        redirect.short_url = short_url

        session.commit()
        return redirect
    finally:
        session.close()


def upsert_page(page_id: Optional[int], title: str, url: str, contents: str, shared: bool) -> Optional[Page]:
    if not url or not url.strip() or not title or not title.strip():
        return None

    url = url.strip().lower().strip('/')
    title = title.strip()
    if contents:
        contents = contents.strip()

    session = db_session.create_session()
    try:
        page = session.query(Page).filter(Page.id == page_id).first()
        if not page:
            page = Page()
            session.add(page)

        page.title = title
        page.url = url
        page.contents = contents
        page.is_shared = shared

        session.commit()
        return page
    finally:
        session.close()


def get_page(url: str, allow_shared=False):
    if not url or not url.strip():
        return None

    session = db_session.create_session()
    try:
        url = url.strip().lower()

        page = session.query(Page).filter(Page.url == url).first()
        if page and not allow_shared and page.is_shared:
            return None

        return page
    finally:
        session.close()


def all_redirects() -> List[Redirect]:
    session = db_session.create_session()
    try:
        return session.query(Redirect).order_by(Redirect.created_date.desc()).all()
    finally:
        session.close()


def all_pages() -> List[Page]:
    session = db_session.create_session()
    try:
        return session.query(Page).order_by(Page.created_date.desc()).all()
    finally:
        session.close()


def get_redirect_by_id(redirect_id: int) -> Optional[Redirect]:
    session = db_session.create_session()
    try:
        return session.query(Redirect).filter(Redirect.id == redirect_id).first()
    finally:
        session.close()


def get_page_by_id(page_id: int) -> Optional[Page]:
    session = db_session.create_session()
    try:
        return session.query(Page).filter(Page.id == page_id).first()
    finally:
        session.close()
