from typing import List

from pypi.db import fake_data


def get_page(url: str) -> dict:
    if url:
        url = url.lower().strip()
    page = fake_data.pages.get(url)
    return page


def get_redirect(url: str) -> dict:
    if url:
        url = url.lower().strip()
    return fake_data.redirects.get(url)


def all_redirects() -> List[dict]:
    return list(fake_data.redirects.values())


def create_redirect(name, short_url, url):
    data = {
        'id': 5,
        'url': url,
        'short_url': short_url,
        'name': name,

    }

    fake_data.redirects[short_url] = data
