import flask
import logbook

from pypi_org.infrastructure.view_modifiers import response
from pypi_org.viewmodels.packages.packagedetails_viewmodel import PackageDetailsViewModel

blueprint = flask.Blueprint('packages', __name__, template_folder='templates')
log = logbook.Logger('Packages')


@blueprint.route('/project/<package_name>')
@response(template_file='packages/details.html')
def package_details(package_name: str):
    vm = PackageDetailsViewModel(package_name)
    if not vm.package:
        log.info(f"Request for {package_name} was not successful, 404.")
        return flask.abort(status=404)

    return vm.to_dict()


@blueprint.route('/<int:rank>')
def popular(rank: int):
    print(type(rank), rank)
    return "The details for the {}th most popular package".format(rank)
