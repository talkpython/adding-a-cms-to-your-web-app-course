import datetime
import sqlalchemy
from pypi.data.modelbase import SqlAlchemyBase


class Page(SqlAlchemyBase):
    __tablename__ = 'pages'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, index=True, default=datetime.datetime.now)
    creating_user = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    url = sqlalchemy.Column(sqlalchemy.String, index=True, nullable=False)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    contents = sqlalchemy.Column(sqlalchemy.String)
