import random
from typing import Optional, Dict, List

from pypi_org.db import fake_data


def get_page(base_url: str) -> Optional[Dict]:
    if not base_url or not base_url.strip():
        return None

    base_url = base_url.strip().lower()

    page = fake_data.pages.get(base_url)
    return page


def get_redirect(base_url: str) -> Optional[Dict]:
    if not base_url or not base_url.strip():
        return None

    base_url = base_url.strip().lower()

    redirect = fake_data.redirects.get(base_url)
    return redirect


def all_pages() -> List[Dict]:
    return list(fake_data.pages.values())


def all_redirects() -> List[Dict]:
    return list(fake_data.redirects.values())


def get_redirect_by_id(redirect_id: int) -> Optional[dict]:
    for url, redirect in fake_data.redirects.items():
        if redirect.get('id') == redirect_id:
            return redirect

    return None


def get_page_by_id(page_id: int) -> Optional[dict]:
    for url, page in fake_data.pages.items():
        if page.get('id') == page_id:
            return page

    return None


def create_redirect(name: str, short_url: str, url: str):
    if get_redirect(short_url):
        raise Exception("Cannot create redirect, exists!")

    data = {
        'id': random.randint(100, 1000000),
        'url': url,
        'short_url': short_url,
        'name': name,
    }

    fake_data.redirects[short_url] = data


def update_redirect(redirect_id, name, short_url, url):
    redirect = get_redirect_by_id(redirect_id)

    if not redirect:
        raise Exception("Cannot update redirect, does not exist!")

    del fake_data.redirects[redirect.get('short_url')]

    redirect['short_url'] = short_url
    redirect['url'] = url
    redirect['name'] = name

    fake_data.redirects[short_url] = redirect
