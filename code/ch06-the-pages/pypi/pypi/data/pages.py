import datetime
import sqlalchemy
from pypi.data.modelbase import SqlAlchemyBase


class Page(SqlAlchemyBase):
    __tablename__ = 'pages'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now, index=True)
    creating_user = sqlalchemy.Column(sqlalchemy.String)

    url = sqlalchemy.Column(sqlalchemy.String, nullable=False, index=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    contents = sqlalchemy.Column(sqlalchemy.String)
