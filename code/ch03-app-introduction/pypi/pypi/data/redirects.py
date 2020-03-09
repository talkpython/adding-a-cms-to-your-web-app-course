import datetime
import sqlalchemy
from pypi.data.modelbase import SqlAlchemyBase


class Redirect(SqlAlchemyBase):
    __tablename__ = 'redirects'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now, index=True)
    creating_user = sqlalchemy.Column(sqlalchemy.String)

    url = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    short_url = sqlalchemy.Column(sqlalchemy.String, index=True, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
