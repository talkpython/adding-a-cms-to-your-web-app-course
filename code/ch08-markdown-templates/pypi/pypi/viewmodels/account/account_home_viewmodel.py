from pyramid.request import Request

from pypi.viewmodels.shared.viewmodel_base import ViewModelBase


class AccountHomeViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)
