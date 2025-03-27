from dependency_injector import containers, providers

from app.internal.repository import Repositories, postgresql
from app.internal.services.cities import CityService
from app.internal.services.definer import DefinerService
from app.internal.services.reports import ReportsService
from app.internal.services.sites import SitesService
from app.internal.services.vectors import VectorService
from app.internal.services.xml_parser import XMLParseService
from app.pkg.settings import settings

__all__ = [
    "Services",
    "ReportsService",
    "VectorService",
    "CityService",
    "XMLParseService",
    "DefinerService",
]


class Services(containers.DeclarativeContainer):
    """Containers with services."""

    configuration = providers.Configuration(
        name="settings",
        pydantic_settings=[settings],
    )

    repositories: postgresql.Repositories = providers.Container(
        Repositories.postgres,
    )

    xml_parse_service = providers.Factory(XMLParseService)
    vector_service = providers.Factory(VectorService, repositories.vectors_repository)
    city_service = providers.Factory(CityService, repositories.city_repository)
    reports_service = providers.Factory(ReportsService, repositories.reports_repository)
    sites_service = providers.Factory(SitesService, repositories.sites_repository)
    definer_service = providers.Factory(DefinerService)
