import logging
from typing import List

from app.internal.repository.postgresql import sites
from app.pkg import models
from app.pkg.logger import get_logger
from app.pkg.models.exceptions.repository import EmptyResult

__all__ = ["SitesService"]


class SitesService:
    __logger: logging.Logger
    repository: sites.SitesRepository

    def __init__(self, sites_repository: sites.SitesRepository):
        self.repository = sites_repository
        self.__logger = get_logger(__name__)

    async def get_sites(self) -> List[models.SiteOut]:
        try:
            return await self.repository.get_list_of_sites()
        except EmptyResult:
            self.__logger.error(f"Empty result while getting all sites")
            return []
        except Exception:
            self.__logger.exception(f"Sudden error while getting all sites")
            return []

    async def get_sites_names(self) -> List[models.SiteIn]:
        try:
            return await self.repository.get_list_of_sites_names()
        except EmptyResult:
            self.__logger.error(f"Empty result while getting all sites")
            return []
        except Exception:
            self.__logger.exception(f"Sudden error while getting all sites")
            return []

    async def add_site(self, site: models.SiteIn) -> models.SiteIn:
        try:
            return await self.repository.add_site(site)
        except EmptyResult:
            self.__logger.error(f"Empty result while adding site")
            return []
        except Exception:
            self.__logger.exception(f"Sudden error while adding site")
            return []

    async def update_site(self, site: models.SiteIn) -> models.SiteIn:
        try:
            return await self.repository.change_site_status(site)
        except EmptyResult:
            self.__logger.error(f"Empty result while updating site")
            return []
        except Exception:
            self.__logger.exception(f"Sudden error while updating site")
            return []
