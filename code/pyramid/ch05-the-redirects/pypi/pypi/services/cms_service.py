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


def get_redirect_by_id(redirect_id):
    if not redirect_id:
        return None

    redirect = None
    for k, r in fake_data.redirects.items():
        if str(r.get('id', '')) == redirect_id:
            redirect = r
            break

    return redirect


def update_redirect(redirect_id, name, short_url, url):
    redirect = get_redirect_by_id(redirect_id)
    if not redirect:
        return

    del fake_data.redirects[redirect['short_url']]

    redirect['name'] = name
    redirect['short_url'] = short_url
    redirect['url'] = url

    fake_data.redirects[short_url] = redirect
