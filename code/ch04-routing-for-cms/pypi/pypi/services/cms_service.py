from pypi.db import fake_data


def get_page(url: str) -> dict:
    page = fake_data.pages.get(url)
    return page


def get_redirect(url: str) -> dict:
    return None
