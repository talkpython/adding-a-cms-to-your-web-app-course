import flask
import logbook

import pypi_org.infrastructure.cookie_auth as cookie_auth
from pypi_org.infrastructure.view_modifiers import response
from pypi_org.services import user_service
from pypi_org.viewmodels.account.index_viewmodel import IndexViewModel
from pypi_org.viewmodels.account.login_viewmodel import LoginViewModel
from pypi_org.viewmodels.account.register_viewmodel import RegisterViewModel

blueprint = flask.Blueprint('account', __name__, template_folder='templates')
log = logbook.Logger('Accounts')


# ################### INDEX #################################


@blueprint.route('/account')
@response(template_file='account/index.html')
def index():
    vm = IndexViewModel()
    if not vm.user:
        return flask.redirect('/account/login')

    log.info(f"User is viewing their account: {vm.user.name} - {vm.user.email}")
    return vm.to_dict()


# ################### REGISTER #################################

@blueprint.route('/account/register', methods=['GET'])
@response(template_file='account/register.html')
def register_get():
    vm = RegisterViewModel()
    return vm.to_dict()


@blueprint.route('/account/register', methods=['POST'])
@response(template_file='account/register.html')
def register_post():
    log.notice(f"Anonymous user is registering for a new account")

    vm = RegisterViewModel()
    vm.validate()

    if vm.error:
        log.notice(f"User could not create account, error: {vm.error}.")
        return vm.to_dict()

    user = user_service.create_user(vm.name, vm.email, vm.password)
    if not user:
        vm.error = 'The account could not be created'
        log.notice(f"User could not create account, error: {vm.error}.")
        return vm.to_dict()

    resp = flask.redirect('/account')
    cookie_auth.set_auth(resp, user.id)

    log.notice(f"User SUCCESSFULLY created account: {user.name} - {user.email}.")
    return resp


# ################### LOGIN #################################

@blueprint.route('/account/login', methods=['GET'])
@response(template_file='account/login.html')
def login_get():
    vm = LoginViewModel()
    return vm.to_dict()


@blueprint.route('/account/login', methods=['POST'])
@response(template_file='account/login.html')
def login_post():
    vm = LoginViewModel()
    vm.validate()

    if vm.error:
        log.notice(f"User could not log in, error: {vm.email} - {vm.error}.")
        return vm.to_dict()

    user = user_service.login_user(vm.email, vm.password)
    if not user:
        vm.error = "The account does not exist or the password is wrong."
        log.notice(f"User could not log in, error: {vm.error}.")
        return vm.to_dict()

    resp = flask.redirect('/account')
    cookie_auth.set_auth(resp, user.id)

    log.notice(f"User SUCCESSFULLY logged in account: {user.name} - {user.email}.")
    return resp


# ################### LOGOUT #################################

@blueprint.route('/account/logout')
def logout():
    user_id = cookie_auth.get_user_id_via_auth_cookie(flask.request)
    user = user_service.find_user_by_id(user_id)
    if user:
        log.notice(f"User {user.email} has logged out.")

    resp = flask.redirect('/')
    cookie_auth.logout(resp)

    return resp
