import os

import pypi
from pypi import DbSession
from pypi.data.pages import Page
from pypi.data.redirects import Redirect


def main():
    init_db()

    load_redirects()
    load_pages()


def load_redirects():
    session = DbSession.create()

    redirect_count = session.query(Redirect).count()
    if redirect_count > 0:
        return

    print(f"Importing {len(redirects)} CMS redirects...")

    for r in redirects:
        redirect = Redirect()
        redirect.short_url = r.get('short_url')
        redirect.url = r.get('url')
        redirect.name = r.get('name')
        redirect.creating_user = 'Michael Kennedy'
        session.add(redirect)

    session.commit()
    session.close()


def load_pages():
    session = DbSession.create()

    page_count = session.query(Page).count()
    if page_count > 0:
        return

    print(f"Importing {len(pages)} CMS pages...")

    for p in pages:
        page = Page()
        page.url = p.get('url')
        page.name = p.get('name')
        page.title = p.get('title')
        page.contents = p.get('contents')
        page.creating_user = 'Michael Kennedy'
        session.add(page)

    session.commit()
    session.close()


def init_db():
    top_folder = os.path.dirname(pypi.__file__)
    rel_file = os.path.join('db', 'pypi.sqlite')
    db_file = os.path.join(top_folder, rel_file)
    DbSession.global_init(db_file)


pages = [
    {
        'url': 'company/history',
        'title': 'Company history',
        'contents': 'Details about company history...',
    },
    {
        'url': 'company/employees',
        'title': 'Our team',
        'contents': 'Details about company employees ...',
    }
]

redirects = [
    {
        'url': 'https://training.talkpython.fm/courses/all',
        'name': 'Courses',
        'short_url': 'courses',
    },
    {
        'url': 'https://pythonbytes.fm/',
        'name': 'Python Bytes',
        'short_url': 'bytes',
    }
]

if __name__ == '__main__':
    main()
