from pyramid.request import Request

from pypi.services import user_service
from pypi.viewmodels.shared.viewmodel_base import ViewModelBase


class AdminHomeViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)
