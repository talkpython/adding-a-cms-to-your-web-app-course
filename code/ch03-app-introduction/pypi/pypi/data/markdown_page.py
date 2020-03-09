import datetime
import sqlalchemy
from pypi.data.modelbase import SqlAlchemyBase


class MarkdownPage(SqlAlchemyBase):
    __tablename__ = 'markdown_pages'

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String, index=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now, index=True)

    is_shared = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, index=True, default=False)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=False)
