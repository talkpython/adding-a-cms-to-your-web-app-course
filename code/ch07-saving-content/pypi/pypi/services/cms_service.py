import random
from typing import List, Optional

from sqlalchemy.orm import Session

from pypi import DbSession
from pypi.data.redirects import Redirect
from pypi.db import fake_data


def get_redirect(url: str) -> Optional[Redirect]:
    if url:
        url = url.lower().strip()

    session: Session = DbSession.create()
    try:
        return session.query(Redirect).filter(Redirect.short_url == url).first()
    finally:
        session.close()


def all_redirects() -> List[Redirect]:
    session: Session = DbSession.create()
    try:
        return session.query(Redirect).order_by(Redirect.created_date.desc())
    finally:
        session.close()


def create_redirect(name: str, short_url: str, url: str, user_email: str):
    session: Session = DbSession.create()

    redirect = Redirect()
    redirect.url = url.strip()
    redirect.short_url = short_url.strip().lower()
    redirect.name = name.strip()
    redirect.creating_user = user_email

    session.add(redirect)
    session.commit()

    return redirect


def get_redirect_by_id(redirect_id: int) -> Optional[Redirect]:
    if not redirect_id:
        return None

    session: Session = DbSession.create()
    try:
        return session.query(Redirect).filter(Redirect.id == redirect_id).first()
    finally:
        session.close()


def update_redirect(redirect_id, name, short_url, url):
    session: Session = DbSession.create()
    try:
        redirect = session.query(Redirect).filter(Redirect.id == redirect_id).first()

        if not redirect:
            return

        redirect.name = name.strip()
        redirect.short_url = short_url.lower().strip()
        redirect.url = url.strip()

        session.commit()
    finally:
        session.close()


def get_page(url: str) -> dict:
    if url:
        url = url.lower().strip()
    page = fake_data.pages.get(url)
    return page


def all_pages():
    return list(fake_data.pages.values())


def get_page_by_id(page_id):
    if not page_id:
        return None

    page = None
    for k, page in fake_data.pages.items():
        if str(page.get('id', '')) == page_id:
            page = page
            break

    return page


def update_page(page_id, title, url, contents):
    page = get_page_by_id(page_id)
    if not page or not url:
        return

    url = url.lower().strip()
    if contents:
        contents = contents.strip()
    if title:
        title = title.strip()

    page['title'] = title
    page['url'] = url
    page['contents'] = contents


def create_page(title, url, contents):
    data = {
        'id': random.randint(5, 10000),
        'url': url,
        'title': title,
        'contents': contents,
    }

    fake_data.pages[url] = data
