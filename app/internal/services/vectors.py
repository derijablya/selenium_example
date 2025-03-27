import logging

from app.internal.repository.postgresql import vectors
from app.pkg import models
from app.pkg.logger import get_logger
from app.pkg.models.exceptions.repository import EmptyResult

__all__ = ["VectorService"]


class VectorService:
    __logger: logging.Logger
    repository: vectors.VectorsRepository

    def __init__(self, vectors_repository: vectors.VectorsRepository):
        self.repository = vectors_repository
        self.__logger = get_logger(__name__)

    async def get_data_by_params(
        self,
        vector_data: models.VectorIn,
    ) -> list[models.VectorOut]:
        try:
            return await self.repository.get_vectors_by_city_url_lang(vector_data)
        except EmptyResult:
            self.__logger.error(
                f"Empty result while getting vectors by city {vector_data.city_is_main} url {vector_data.site_url} lang {vector_data.lang}",
            )
            return []
        except Exception:
            self.__logger.exception(
                f"Sudden error while getting vectors by city {vector_data.city_is_main} url {vector_data.site_url} lang {vector_data.lang}",
            )
            return []

    async def get_vector_text(
        self,
        vector_data: models.VectorTextIn,
    ) -> models.VectorNamesTextOut:
        try:
            return await self.repository.get_vector_text(vector_data)
        except EmptyResult:
            self.__logger.error(
                f"Empty result while getting vector text by city_is_main {vector_data.city_is_main} url {vector_data.site_url} lang {vector_data.lang} from {vector_data.from_v} to {vector_data.to_v}",
            )
            return ""
        except Exception:
            self.__logger.exception(
                f"Sudden error while getting vector text by city_is_main {vector_data.city_is_main} url {vector_data.site_url} lang {vector_data.lang} from {vector_data.from_v} to {vector_data.to_v}",
            )
            return ""

    async def add_vector_data(self, vector_data: models.Vector) -> models.Vector:
        try:
            return await self.repository.add_vector(vector_data)
        except EmptyResult:
            self.__logger.error(f"Empty result while adding vector")
            return None
        except Exception:
            self.__logger.exception(f"Sudden error while adding vector")
            return None
