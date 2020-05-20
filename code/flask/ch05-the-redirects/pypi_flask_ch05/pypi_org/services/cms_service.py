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
