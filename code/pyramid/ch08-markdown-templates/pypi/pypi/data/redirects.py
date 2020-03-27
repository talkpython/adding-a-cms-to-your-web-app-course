import datetime
import sqlalchemy
from pypi.data.modelbase import SqlAlchemyBase


class Redirect(SqlAlchemyBase):
    __tablename__ = 'redirects'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, index=True, default=datetime.datetime.now)
    creating_user = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    short_url = sqlalchemy.Column(sqlalchemy.String, index=True, nullable=False)
    url = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
