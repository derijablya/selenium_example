from dependency_injector import containers, providers

from app.internal.services import Services
from app.internal.workers.generator import GeneratorService
from app.internal.workers.link_former import LinkService
from app.internal.workers.site_validator import SiteValidator
from app.pkg.settings import settings


class Workers(containers.DeclarativeContainer):
    """Containers with services."""

    configuration = providers.Configuration(
        name="settings",
        pydantic_settings=[settings],
    )
    services: Services = providers.Container(Services)

    link_service_worker = providers.Factory(LinkService)
    generator_service_worker = providers.Factory(GeneratorService)
    site_validator_worker = providers.Factory(
        SiteValidator,
        services.reports_service,
        services.vector_service,
        services.city_service,
        services.sites_service,
    )
