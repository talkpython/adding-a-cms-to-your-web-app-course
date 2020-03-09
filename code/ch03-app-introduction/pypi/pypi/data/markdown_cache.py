import datetime
import sqlalchemy
from pypi.data.modelbase import SqlAlchemyBase


class MarkdownCache(SqlAlchemyBase):
    __tablename__ = 'markdown_cache'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    key = sqlalchemy.Column(sqlalchemy.String, index=True)
    type = sqlalchemy.Column(sqlalchemy.String, index=True)
    name = sqlalchemy.Column(sqlalchemy.String, index=True)
    contents = sqlalchemy.Column(sqlalchemy.String)

    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now, index=True)
