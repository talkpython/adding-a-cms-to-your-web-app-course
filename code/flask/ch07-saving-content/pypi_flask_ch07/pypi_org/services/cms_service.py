import random
from typing import Optional, Dict, List

from pypi_org.data import db_session
from pypi_org.data.redirects import Redirect
from pypi_org.db import fake_data


def get_page(base_url: str) -> Optional[Dict]:
    if not base_url or not base_url.strip():
        return None

    base_url = base_url.strip().lower()

    page = fake_data.pages.get(base_url)
    return page


def get_redirect(base_url: str) -> Optional[Redirect]:
    if not base_url or not base_url.strip():
        return None

    base_url = base_url.strip().lower()

    session = db_session.create_session()
    try:
        return session.query(Redirect).filter(Redirect.short_url == base_url).first()
    finally:
        session.close()


def all_pages() -> List[Dict]:
    return list(fake_data.pages.values())


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


def get_page_by_id(page_id: int) -> Optional[dict]:
    for url, page in fake_data.pages.items():
        if page.get('id') == page_id:
            return page

    return None


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


def create_page(title, url, contents):
    if get_page(url):
        raise Exception("Cannot create page, exists!")

    data = {
        'id': random.randint(100, 1000000),
        'url': url,
        'title': title,
        'contents': contents,
    }

    fake_data.pages[url] = data


def update_page(page_id: int, title: str, url: str, contents: str):
    page = get_page_by_id(page_id)

    if not page:
        raise Exception("Cannot update page, does not exist!")

    del fake_data.pages[page.get('url')]

    page['title'] = title.strip()
    page['url'] = url.strip().lower()
    page['contents'] = contents.strip()

    fake_data.pages[url] = page
