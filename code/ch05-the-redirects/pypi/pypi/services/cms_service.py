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
