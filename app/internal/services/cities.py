import logging
from typing import List

from app.internal.repository.postgresql import cities
from app.pkg import models
from app.pkg.logger import get_logger
from app.pkg.models.exceptions.repository import EmptyResult

__all__ = ["CityService"]


class CityService:
    __logger: logging.Logger
    repository: cities.CitiesRepository

    def __init__(self, cities_repository: cities.CitiesRepository):
        self.repository = cities_repository
        self.__logger = get_logger(__name__)

    async def get_cities(self) -> list[models.City]:
        try:
            return await self.repository.get_cities_all()
        except EmptyResult:
            self.__logger.error(f"Empty result while getting all cities")
            return []
        except Exception:
            self.__logger.exception(f"Sudden error while getting all cities")
            return []

    async def get_cities_by_code(self, code: str) -> List[models.CityNameLangIsMain]:
        try:
            res = await self.repository.get_city_by_code_db(code)
            return res
        except EmptyResult:
            self.__logger.error(f"Empty result while getting city by code {code}")
            return []
        except Exception:
            self.__logger.exception(f"Sudden error while getting city by code {code}")
            return []

    async def add_city_data(self, city_data: models.City) -> models.City:
        try:
            return await self.repository.add_city(city_data)
        except EmptyResult:
            self.__logger.error(f"Empty result while adding city")
            return None
        except Exception:
            self.__logger.exception(f"Sudden error while adding city")
            return None
