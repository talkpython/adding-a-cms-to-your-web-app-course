from typing import Optional

import flask
from flask import Request

from pypi_org.data.users import User
from pypi_org.infrastructure import request_dict, cookie_auth
from pypi_org.services import user_service


class ViewModelBase:
    def __init__(self):
        self.request: Request = flask.request
        self.__user: Optional[User] = None
        self.__user_set: bool = False
        self.request_dict = request_dict.create('')

        self.error: Optional[str] = None
        self.user_id: Optional[int] = cookie_auth.get_user_id_via_auth_cookie(self.request)

    def to_dict(self):
        data = dict(self.__dict__)
        data['user'] = self.user

        return data

    @property
    def user(self) -> Optional[User]:
        if self.__user or self.__user_set:
            return self.__user

        self.__user_set = True

        if not self.user_id:
            return None

        self.__user = user_service.find_user_by_id(self.user_id)
        return self.__user
