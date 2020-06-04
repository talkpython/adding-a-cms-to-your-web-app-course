import datetime

import sqlalchemy

from pypi_org.data.modelbase import SqlAlchemyBase


class Redirect(SqlAlchemyBase):
    __tablename__ = 'redirects'

    id: int = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    # admin data
    created_date: datetime.datetime = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now, index=True)
    creating_user: str = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    # direct data
    short_url: str = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True, index=True)
    url: str = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    name: str = sqlalchemy.Column(sqlalchemy.String, nullable=False)
