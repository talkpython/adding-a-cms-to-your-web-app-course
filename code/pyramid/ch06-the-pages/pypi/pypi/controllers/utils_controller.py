from pyramid.view import view_config, notfound_view_config

from pypi.viewmodels.shared.viewmodel_base import ViewModelBase
from pypi.viewmodels.utils.sitemap_viewmodel import SiteMapViewModel


# ################### Sitemap #################################

@view_config(route_name='sitemap.xml', renderer='pypi:templates/utils/sitemap_xml.pt')
def sitemap(request):
    vm = SiteMapViewModel(request, 1000)
    request.response.content_type = 'application/xml'
    return vm.to_dict()


# ################### Robots #################################

@view_config(route_name='robots.txt', renderer='pypi:templates/utils/robots.pt')
def robots(request):
    request.response.content_type = 'text/plain'
    return {}


# ################### Not Found #################################

@notfound_view_config(renderer='pypi:templates/utils/404.pt')
def robots(request):
    request.response.status = 404
    return ViewModelBase(request).to_dict()
