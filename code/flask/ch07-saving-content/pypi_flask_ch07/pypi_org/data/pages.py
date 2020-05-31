import datetime

import sqlalchemy

from pypi_org.data.modelbase import SqlAlchemyBase


class Page(SqlAlchemyBase):
    __tablename__ = 'pages'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    # admin data
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now, index=True)
    creating_user = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    # direct data
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    url = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True, index=True)
    contents = sqlalchemy.Column(sqlalchemy.String)
