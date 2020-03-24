import sqlalchemy
import sqlalchemy.orm
from sqlalchemy.orm import Session

from pypi.data.modelbase import SqlAlchemyBase
# noinspection PyUnresolvedReferences
import pypi.data.__all_models


class DbSession:
    __factory = None
    __engine = None
    is_initialized = False

    @staticmethod
    def global_init(db_file: str):
        if DbSession.__factory:
            return

        if not db_file or not db_file.strip():
            raise Exception("You must specify a data file.")

        conn_str = f'sqlite:///{db_file}?check_same_thread=False'
        print(f"Connecting to DB at: {conn_str}")

        engine = sqlalchemy.create_engine(conn_str, echo=False)
        DbSession.__engine = engine
        DbSession.__factory = sqlalchemy.orm.sessionmaker(bind=engine)

        SqlAlchemyBase.metadata.create_all(engine)
        DbSession.is_initialized = True

    @staticmethod
    def create() -> Session:
        session: Session = DbSession.__factory()
        session.expire_on_commit = False
        return session
