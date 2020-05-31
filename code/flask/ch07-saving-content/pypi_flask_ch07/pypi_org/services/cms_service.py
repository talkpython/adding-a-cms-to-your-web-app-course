from typing import Optional, List

from pypi_org.data import db_session
from pypi_org.data.pages import Page
from pypi_org.data.redirects import Redirect


def get_page(base_url: str) -> Optional[Page]:
    if not base_url or not base_url.strip():
        return None

    base_url = base_url.strip().lower()

    session = db_session.create_session()
    try:
        return session.query(Page).filter(Page.url == base_url).first()
    finally:
        session.close()


def get_redirect(base_url: str) -> Optional[Redirect]:
    if not base_url or not base_url.strip():
        return None

    base_url = base_url.strip().lower()

    session = db_session.create_session()
    try:
        return session.query(Redirect).filter(Redirect.short_url == base_url).first()
    finally:
        session.close()


def all_pages() -> List[Page]:
    session = db_session.create_session()
    try:
        return session.query(Page).order_by(Page.created_date.desc()).all()
    finally:
        session.close()


def all_redirects() -> List[Redirect]:
    session = db_session.create_session()
    try:
        return session.query(Redirect).order_by(Redirect.created_date.desc()).all()
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


def create_redirect(name: str, short_url: str, url: str, user_email: str) -> Redirect:
    if get_redirect(short_url):
        raise Exception("Cannot create redirect, exists!")

    redirect = Redirect()
    redirect.url = url.strip()
    redirect.short_url = short_url.strip().lower()
    redirect.name = name.strip()
    redirect.creating_user = user_email

    session = db_session.create_session()
    try:
        session.add(redirect)
        session.commit()
        return redirect
    finally:
        session.close()


def update_redirect(redirect_id, name, short_url, url) -> Redirect:
    if not get_redirect_by_id(redirect_id):
        raise Exception("Cannot update redirect, does not exist!")

    session = db_session.create_session()
    try:
        redirect = session.query(Redirect).filter(Redirect.id == redirect_id).first()
        redirect.name = name
        redirect.short_url = short_url
        redirect.url = url

        session.commit()
        return redirect
    finally:
        session.close()


def create_page(title: str, url: str, contents: str, creating_user: str) -> Page:
    if get_page(url):
        raise Exception("Cannot create page, exists!")

    session = db_session.create_session()
    try:
        page = Page()
        page.title = title.strip()
        page.contents = contents.strip()
        page.url = url.strip().lower()
        page.creating_user = creating_user

        session.add(page)
        session.commit()

        return page

    finally:
        session.close()


def update_page(page_id: int, title: str, url: str, contents: str) -> Page:
    session = db_session.create_session()
    try:
        page = session.query(Page).filter(Page.id == page_id).first()
        if not page:
            raise Exception("Cannot update page, does not exist!")

        page.title = title.strip()
        page.contents = contents.strip()
        page.url = url.strip().lower()

        session.commit()

        return page

    finally:
        session.close()
