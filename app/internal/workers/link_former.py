import logging

from dependency_injector.wiring import Provide, inject

from app.internal.services import Services, xml_parser
from app.internal.services.cities import CityService
from app.internal.services.vectors import VectorService
from app.pkg import models
from app.pkg.logger import get_logger


class LinkService:
    logger: logging.Logger

    def __init__(self):
        self.__logger = get_logger(__name__)

    def __form_link(self, data: models.FormUrlIn) -> models.FormUrlOut:
        if data.site_url == "example1":
            if data.lang == "ru":
                return models.FormUrlOut(
                    url=f"{data.site_url}/exchange-{data.from_v}-to-{data.to_v}-{data.city_code}/",
                )
            else:
                return models.FormUrlOut(
                    url=f"{data.site_url}/{data.lang}/exchange-{data.from_v}-to-{data.to_v}-{data.city_code}/",
                )
        elif data.site_url == "example2":
            if data.lang == "ru":
                return models.FormUrlOut(
                    url=f"{data.site_url}/exchange-{data.from_v}-to-{data.to_v}-{data.city_code}/",
                )
            else:
                return models.FormUrlOut(
                    url=f"{data.site_url}/{data.lang}/exchange-{data.from_v}-to-{data.to_v}-{data.city_code}/",
                )

    @inject
    async def process_starter(
        self,
        site_url: str,
        city_service: CityService = Provide[Services.city_service],
        vectors_service: VectorService = Provide[Services.vector_service],
    ) -> list[models.LinkFormerData]:
        """
        Algorithm:
        1. Get vectors + cities from xml
        2. Get city's data from db
        3. Get vectors from db by lang, is_main flag, site_url
        """
        list_of_vectors_cities: list[
            models.XMLParsedVector
        ] = await xml_parser.XMLParseService.parse_xml()
        """!!!

        Result list !!!
        """
        list_data_for_validation: list[models.LinkFormerData] = []

        for vector_city in list_of_vectors_cities:
            current_list_city_langs: list[
                models.CityNameLangIsMain
            ] = await city_service.get_cities_by_code(vector_city.city_code)

            if current_list_city_langs:
                for lang in current_list_city_langs:
                    current_text: models.VectorNamesTextOut = (
                        await vectors_service.get_vector_text(
                            models.VectorTextIn(
                                city_is_main=lang.city_is_main,
                                site_url=site_url,
                                lang=lang.city_lang,
                                from_v=vector_city.from_v,
                                to_v=vector_city.to_v,
                            ),
                        )
                    )
                    if current_text:
                        current_url: models.FormUrlOut = self.__form_link(
                            models.FormUrlIn(
                                site_url=site_url,
                                from_v=vector_city.from_v,
                                to_v=vector_city.to_v,
                                lang=lang.city_lang,
                                city_code=vector_city.city_code,
                            ),
                        )
                        data_for_validation = models.LinkFormerData(
                            url=current_url.url,
                            city_name=lang.city_name,
                            city_code=vector_city.city_code,
                            city_code_name=lang.city_code_name,
                            from_code=vector_city.from_v,
                            from_name=current_text.from_name,
                            to_code=vector_city.to_v,
                            to_name=current_text.to_name,
                            in_v=vector_city.in_v,
                            out_v=vector_city.out_v,
                            amount_v=vector_city.amount_v,
                            minamount_v=vector_city.minamount_v,
                            maxamount_v=vector_city.maxamount_v,
                            text_v=current_text.text_v,
                            lang=lang.city_lang,
                            site_url=site_url,
                        )
                        list_data_for_validation.append(data_for_validation)

                    else:
                        self.__logger.exception("error")

            else:
                self.__logger.exception("error")
        return list_data_for_validation
