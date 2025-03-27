from dependency_injector import containers, providers

from .cities import CitiesRepository
from .reports import ReportsRepository
from .sites import SitesRepository
from .vectors import VectorsRepository


class Repositories(containers.DeclarativeContainer):
    vectors_repository = providers.Factory(VectorsRepository)
    city_repository = providers.Factory(CitiesRepository)
    reports_repository = providers.Factory(ReportsRepository)
    sites_repository = providers.Factory(SitesRepository)
