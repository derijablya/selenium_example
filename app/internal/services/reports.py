import logging
from typing import List

from app.internal.repository.postgresql import reports
from app.pkg import models
from app.pkg.logger import get_logger
from app.pkg.models.base import BaseException
from app.pkg.models.exceptions.repository import EmptyResult

__all__ = ["ReportsService"]


class ReportsService:
    __logger: logging.Logger
    repository: reports.ReportsRepository

    def __init__(self, reports_repository: reports.ReportsRepository):
        self.__logger = get_logger(__name__)
        self.repository = reports_repository

    async def upsert_report(self, report_data: models.SeleniumOutReport) -> None:
        try:
            services_str = '{"' + '", "'.join(report_data.services) + '"}'
            data_str = f"""('{report_data.url}',
                        '{report_data.from_code}',
                        '{report_data.to_code}', 
                        '{report_data.city_code}', 
                        '{report_data.lang}', 
                        {report_data.min_value_selenium}, 
                        {report_data.min_value_db}, 
                        {report_data.min_valid}, 
                        {report_data.max_value_selenium}, 
                        {report_data.max_value_db}, 
                        {report_data.max_valid}, 
                        {report_data.in_value_selenium}, 
                        {report_data.in_value_db}, 
                        {report_data.in_valid}, 
                        {report_data.out_value_selenium}, 
                        {report_data.out_value_db}, 
                        {report_data.out_valid}, 
                        {report_data.texts}, 
                        '{services_str}', 
                        '{report_data.date_time}'::timestamp,
                        {report_data.fatal},
                        '{report_data.site_url}')"""
            self.__logger.info("Adding report: %s", data_str)
            await self.repository.add_report(cmd=data_str)
        except EmptyResult:
            self.__logger.exception("Empty result while adding report")

        except BaseException as e:
            self.__logger.exception(e)

        except Exception as e:
            self.__logger.exception(e)

    @staticmethod
    async def __fit_in_format(
        report_data: models.SeleniumOutReport,
    ) -> models.ReportOut:
        result: models.ReportOut = models.ReportOut(
            site_url=report_data.site_url,
            vectors=[
                models.VectorOutReport(
                    from_code=report_data.from_code,
                    to_code=report_data.to_code,
                    cities=[
                        models.CityOutReport(
                            city_code=report_data.city_code,
                            langs=[
                                models.LanguageOutReport(
                                    lang=report_data.lang,
                                    info=models.InfoOutReport(
                                        min_info=models.NumberDataOutReport(
                                            fact_value=report_data.min_value_selenium,
                                            expected_value=report_data.min_value_db,
                                            valid=report_data.min_valid,
                                        ),
                                        max_info=models.NumberDataOutReport(
                                            fact_value=report_data.max_value_selenium,
                                            expected_value=report_data.max_value_db,
                                            valid=report_data.max_valid,
                                        ),
                                        in_info=models.NumberDataOutReport(
                                            fact_value=report_data.in_value_selenium,
                                            expected_value=report_data.in_value_db,
                                            valid=report_data.in_valid,
                                        ),
                                        out_info=models.NumberDataOutReport(
                                            fact_value=report_data.out_value_selenium,
                                            expected_value=report_data.out_value_db,
                                            valid=report_data.out_valid,
                                        ),
                                        texts=report_data.texts,
                                        services=report_data.services,
                                        fatal=report_data.fatal,
                                        last_time_checked=report_data.date_time,
                                        current_page_url=report_data.url,
                                    ),
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )
        return result

    async def __fit_list_in_format(
        self,
        report_data: List[models.SeleniumOutReport],
    ) -> List[models.ReportOut]:
        list_sites = []
        list_result: List[models.ReportOut] = []
        for report in report_data:
            if report.site_url not in list_sites:
                list_sites.append(report.site_url)
        for site in list_sites:
            vectors = []
            current_vectors: List[models.VectorOutReport] = []
            current_site: models.ReportOut
            list_of_reports_for_site = []
            for report in report_data:
                if report.site_url == site:
                    list_of_reports_for_site.append(report)
                    if f"{report.from_code}-to-{report.to_code}" not in vectors:
                        vectors.append(f"{report.from_code}-to-{report.to_code}")
            for vector in vectors:
                cities = []
                current_cities: List[models.CityOutReport] = []
                current_vector: models.VectorOutReport
                list_of_reports_for_vector = []
                for report in list_of_reports_for_site:
                    if f"{report.from_code}-to-{report.to_code}" == vector:
                        list_of_reports_for_vector.append(report)
                        if report.city_code not in cities:
                            cities.append(report.city_code)
                for city in cities:
                    languages = []
                    current_langs: List[models.LanguageOutReport] = []
                    current_city: models.CityOutReport
                    list_of_reports_for_city = []
                    for report in list_of_reports_for_vector:
                        if report.city_code == city:
                            list_of_reports_for_city.append(report)
                            if report.lang not in languages:
                                languages.append(report.lang)
                    for language in languages:
                        current_report: models.SeleniumOutReport
                        for report in list_of_reports_for_city:
                            if report.lang == language:
                                current_lang = models.LanguageOutReport(
                                    lang=report.lang,
                                    info=models.InfoOutReport(
                                        min_info=models.NumberDataOutReport(
                                            fact_value=report.min_value_selenium,
                                            expected_value=report.min_value_db,
                                            valid=report.min_valid,
                                        ),
                                        max_info=models.NumberDataOutReport(
                                            fact_value=report.max_value_selenium,
                                            expected_value=report.max_value_db,
                                            valid=report.max_valid,
                                        ),
                                        in_info=models.NumberDataOutReport(
                                            fact_value=report.in_value_selenium,
                                            expected_value=report.in_value_db,
                                            valid=report.in_valid,
                                        ),
                                        out_info=models.NumberDataOutReport(
                                            fact_value=report.out_value_selenium,
                                            expected_value=report.out_value_db,
                                            valid=report.out_valid,
                                        ),
                                        texts=report.texts,
                                        services=report.services,
                                        fatal=report.fatal,
                                        last_time_checked=report.date_time,
                                        current_page_url=report.url,
                                    ),
                                )
                                current_langs.append(current_lang)
                    current_city = models.CityOutReport(
                        city_code=city,
                        langs=current_langs,
                    )
                    current_cities.append(current_city)
                current_vector = models.VectorOutReport(
                    from_code=vector.split("-to-")[0],
                    to_code=vector.split("-to-")[1],
                    cities=current_cities,
                )
                current_vectors.append(current_vector)
            current_site = models.ReportOut(site_url=site, vectors=current_vectors)
            list_result.append(current_site)

        return list_result

    async def get_report(self, report: models.ReportIn) -> models.ReportOut:
        try:
            self.__logger.info(f"Getting report for {report}")
            res: models.SeleniumOutReport = await self.repository.get_report(report)

            self.__logger.info(f"Got report for {res}")
            result_fit = await self.__fit_in_format(res)
            self.__logger.info(f"Fit report for {result_fit}")
            return result_fit
        except EmptyResult:
            self.__logger.error("Empty result while getting report")
        except Exception as e:
            self.__logger.exception(e)

    async def get_report_raw_result(
        self,
        report: models.ReportIn,
    ) -> models.SeleniumOutReport:
        try:
            res: models.SeleniumOutReport = await self.repository.get_report(report)
            return res
        except EmptyResult:
            self.__logger.error("Empty result while getting report")
        except Exception as e:
            self.__logger.exception(e)

    async def get_all_reports(self) -> List[models.ReportOut]:
        try:
            res_raw = await self.repository.get_reports()
            result_only_invalid: List[models.SeleniumOutReport] = []
            for report in res_raw:
                if (
                    not report.min_valid
                    or not report.max_valid
                    or not report.in_valid
                    or not report.out_valid
                ):
                    result_only_invalid.append(report)
            result_fit = await self.__fit_list_in_format(result_only_invalid)
            return result_fit
        except EmptyResult:
            self.__logger.error("Empty result while getting all reports")
        except Exception as e:
            self.__logger.exception(e)
        return []
