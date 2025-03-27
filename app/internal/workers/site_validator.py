import asyncio
import datetime
from typing import List

import aiohttp
from celery import group, shared_task
from dependency_injector.wiring import Provide, inject

from app.internal import services
from app.internal.services import Services, cities, reports, sites, vectors
from app.internal.services.reports import ReportsService
from app.internal.workers import link_former
from app.pkg import models, settings
from app.pkg.logger import get_logger
from app.pkg.settings import settings

__all__ = ["SiteValidator"]


class SiteValidator:
    cities: cities.CityService
    reports: reports.ReportsService
    vectors: vectors.VectorService
    sites: sites.SitesService

    def __init__(
        self,
        reports_service: services.ReportsService,
        vectors_service: services.VectorService,
        city_service: services.CityService,
        sites_service: services.SitesService,
    ):
        offset = datetime.timedelta(hours=3)
        self.tz = datetime.timezone(offset, name="MSK")
        self.__logger = get_logger(__name__)
        self.res_text_page1 = False
        self.res_services = []
        self.res_min_valid = False
        self.res_min_value: float = 0
        self.res_max_valid = False
        self.res_max_value: float = 0
        self.res_course_in_valid = False
        self.res_course_out_valid = False
        self.res_course_in_value: float = 0
        self.res_course_out_value: float = 0
        self.res_text_page2 = False
        self.res_info_page2 = False
        self.res_info_page3 = False
        self.res_fatal = False
        self.texts_valid = False
        self.current_result_model: dict = {}
        self.reports_service = reports_service
        self.vectors_service = vectors_service
        self.city_service = city_service
        self.sites_service = sites_service

    async def serialize_dict_and_run_attempt_send_request(self, data_raw: dict):
        data: models.LinkFormerData = models.LinkFormerData(**data_raw)
        if data.site_url == "example1":
            current_test = class_example1(
                site_data=data,
                reports_service=self.reports_service,
                vectors_service=self.vectors_service,
                city_service=self.city_service,
                sites_service=self.sites_service,
            )
            result_for_url: models.SeleniumOutReport = current_test.run_check()
        elif data.site_url == "example2":
            current_test = class_example2(
                site_data=data,
                reports_service=self.reports_service,
                vectors_service=self.vectors_service,
                city_service=self.city_service,
                sites_service=self.sites_service,
            )
            result_for_url: models.SeleniumOutReport = current_test.run_check()

        else:
            raise ValueError(f"Unknown site: {data.site_url}")
        return result_for_url.dict()

    async def starter(self):
        list_of_sites: List[models.SiteOut] = await self.sites_service.get_sites()
        list_of_data_for_sites = []
        full_period = float(settings.FULL_CHECK_INTERVAL)

        for site in list_of_sites:
            if site.site_status:
                list_current_site = await self.validate_sharded(site.site_url)
                for site in list_current_site:
                    list_of_data_for_sites.append(site)

        amount_of_sites = len(list_of_data_for_sites)
        if amount_of_sites == 0:
            raise ValueError("No sites for validation")
        interval = full_period / amount_of_sites
        current_interval = 0
        list_of_data_for_tasks = []
        for site in list_of_data_for_sites:
            current_interval += interval
            list_of_data_for_tasks.append((site, current_interval))
        aggregate_check.delay(list_of_data_for_tasks)

    async def validate_sharded(
        self,
        site_url: str,
    ):
        list_of_data_for_validation: List[
            models.LinkFormerData
        ] = await link_former.LinkService().process_starter(site_url)
        len_of_list = len(list_of_data_for_validation)
        list_of_data_for_tasks = []
        for i in range(len_of_list):
            # async with aiohttp.ClientSession() as session:
            #     async with session.get(list_of_data_for_validation[i].url) as resp:
            #         res = resp.status
            #         if res == 404:
            #             self.__logger.exception(
            #                 f"404: {list_of_data_for_validation[i].url}",
            #             )
            #             continue
            # async with aiohttp.ClientSession() as session:
            #     async with session.get(
            #             f"http://{settings.SELENIUM_HOST}:4444/wd/hub/status"
            #     ) as resp:
            #         res = await resp.json()
            #         status_selenium: bool = res["value"]["ready"]
            #         if not status_selenium:
            #             self.__logger.exception(f"!!!-Selenium is fallen-!!!")
            #             break
            site = list_of_data_for_validation[i]
            list_of_data_for_tasks.append(site.dict())

        return list_of_data_for_tasks

    @inject
    async def start_new_check(
        self,
        report: models.ReportIn,
        reports_service: ReportsService = Provide[Services.reports_service],
    ):
        report_plus_https: models.ReportIn = models.ReportIn(
            site_url=f"https://{report.site_url}",
            from_code=report.from_code,
            to_code=report.to_code,
            city_code=report.city_code,
            lang=report.lang,
        )
        res: models.SeleniumOutReport = await reports_service.get_report_raw_result(
            report,
        )
        list_of_data: List[
            models.LinkFormerData
        ] = await link_former.LinkService().process_starter(report_plus_https.site_url)
        current_report: models.LinkFormerData = list_of_data[0]

        for data in list_of_data:
            if (
                data.from_code == res.from_code
                and data.to_code == res.to_code
                and data.city_code == res.city_code
                and data.lang == res.lang
            ):
                current_report: models.LinkFormerData = data
                break
        self.__logger.info(f"Current report: {current_report}")
        res = unscheduled_check.delay(data=current_report.dict()).get()
        res_model = models.SeleniumOutReport(**res)
        await self.reports_service.upsert_report(report_data=res_model)


@shared_task(name="recheck_error")
def recheck_error(data):
    return asyncio.run(
        SiteValidator(
            Services.reports_service,
            Services.vector_service,
            Services.city_service,
        ).serialize_dict_and_run_attempt_send_request(data),
    )


@shared_task(name="recheck_url", max_retries=3, auto_retry_for=(Exception,))
def recheck_url(data):
    return asyncio.run(
        SiteValidator(
            Services.reports_service,
            Services.vector_service,
            Services.city_service,
        ).serialize_dict_and_run_attempt_send_request(data),
    )


@shared_task(name="unscheduled_check", max_retries=3, auto_retry_for=(Exception,))
def unscheduled_check(data):
    return asyncio.run(
        SiteValidator(
            Services.reports_service,
            Services.vector_service,
            Services.city_service,
            Services.sites_service,
        ).serialize_dict_and_run_attempt_send_request(data),
    )


@shared_task(name="unscheduled_check_db", max_retries=3, auto_retry_for=(Exception,))
def unscheduled_check_db(data):
    res = asyncio.run(
        SiteValidator(
            Services.reports_service,
            Services.vector_service,
            Services.city_service,
            Services.sites_service,
        ).serialize_dict_and_run_attempt_send_request(data),
    )
    if res["fatal"]:
        unscheduled_check_db.delay(data)
    add_report_to_db.delay(res)


@shared_task(name="aggregate_check")
def aggregate_check(data):
    list_of_tasks = []
    for link in data:
        list_of_tasks.append(unscheduled_check_db.s(link[0]).set(countdown=link[1]))
    group(list_of_tasks)()


@shared_task(name="add_report_to_db")
def add_report_to_db(data):
    asyncio.run(add_report_request(data))


async def add_report_request(data):
    headers = {"X-ACCESS-TOKEN": settings.X_API_TOKEN.get_secret_value()}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(
            "http://sites_text_validator__api:5000/add_report_data",
            json=models.SeleniumOutReport(**data).dict(exclude={"date_time"}),
        ) as resp:
            await resp.json()


async def start_new_check_request():
    headers = {"X-ACCESS-TOKEN": settings.X_API_TOKEN.get_secret_value()}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(
            "http://sites_text_validator__api:5000/start_full_check",
        ) as resp:
            await resp.json()
