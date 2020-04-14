from typing import Callable, Optional

import logbook
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session

from pypi_org.data.modelbase import SqlAlchemyBase

__factory: Optional[Callable[[], Session]] = None
is_initialized = False

log = logbook.Logger('db_session')


def global_init(db_file: str):
    global __factory, is_initialized
    log.info("Initializing")

    if __factory:
        log.info("Already initialized, skipping reinit.")
        return

    if not db_file or not db_file.strip():
        raise Exception("You must specify a db file.")

    conn_str = 'sqlite:///' + db_file.strip()
    log.notice("Connecting to DB with {}".format(conn_str))

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    # noinspection PyUnresolvedReferences
    import pypi_org.data.__all_models

    SqlAlchemyBase.metadata.create_all(engine)
    is_initialized = True


def create_session() -> Session:
    global __factory

    if not __factory:
        raise Exception("You must call global init before you can continue.")

    session = __factory()
    session.expire_on_commit = False
    return session
