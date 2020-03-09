from typing import Optional

from pyramid.request import Request

from pypi.data.users import User
from pypi.infrastructure import request_dict, cookie_auth
from pypi.services import user_service


class ViewModelBase:
    def __init__(self, request: Request):
        self.__user = None
        self.__user_set = False
        self.request = request
        self.request_dict = request_dict.create(request)
        self.error: Optional[str] = None
        self.user_id: Optional[int] = cookie_auth.get_user_id_via_auth_cookie(request)

    def to_dict(self):
        data = dict(self.__dict__)
        data['user'] = self.user

        return data

    @property
    def user(self) -> Optional[User]:
        if self.__user_set:
            return self.__user

        self.__user_set = True

        if not self.user_id:
            return None

        self.__user = user_service.find_user_by_id(self.user_id)
        return self.__user
