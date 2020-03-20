import random
from typing import List, Optional

from sqlalchemy.orm import Session

from pypi import DbSession
from pypi.data.pages import Page
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
        return session.query(Redirect).order_by(Redirect.created_date.desc()).all()
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


def get_page(url: str) -> Optional[Page]:
    if url:
        url = url.lower().strip()

    session = DbSession.create()
    try:
        return session.query(Page).filter(Page.url == url).first()
    finally:
        session.close()


def all_pages():
    session = DbSession.create()
    try:
        return session.query(Page).order_by(Page.created_date.desc()).all()
    finally:
        session.close()


def get_page_by_id(page_id: int) -> Optional[Page]:
    if not page_id:
        return None

    session = DbSession.create()
    try:
        return session.query(Page).filter(Page.id == id).first()
    finally:
        session.close()


def update_page(page_id, title, url, contents):
    session = DbSession.create()
    try:
        page = session.query(Page).filter(Page.url == url).first()
        if not page or not url:
            return

        url = url.lower().strip()
        if contents:
            contents = contents.strip()
        if title:
            title = title.strip()

        page.title = title
        page.url = url
        page.contents = contents

        session.commit()

    finally:
        session.close()


def create_page(title, url, contents):
    session = DbSession.create()
    url = url.lower().strip()
    if contents:
        contents = contents.strip()
    if title:
        title = title.strip()

    page = Page()
    page.title = title
    page.url = url
    page.contents = contents
    session.add(page)

    session.commit()
