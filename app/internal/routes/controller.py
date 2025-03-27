from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, BackgroundTasks, Depends
from starlette import status

from app.internal.services import ReportsService, Services, SitesService
from app.internal.workers import Workers
from app.internal.workers.site_validator import SiteValidator
from app.pkg.models import ReportIn, ReportOut, SiteIn, StatusModel

__all__ = ["router"]

router = APIRouter(tags=["Get info"])


@router.post(
    "/refresh_report",
    response_model=StatusModel,
    status_code=status.HTTP_200_OK,
    description="Start new check for page",
)
@inject
async def refresh_report(
    item: ReportIn,
    background_tasks: BackgroundTasks,
    worker: SiteValidator = Depends(Provide[Workers.site_validator_worker]),
):
    background_tasks.add_task(worker.start_new_check, item)
    return StatusModel(status="ok")


@router.get(
    "/site_data_list",
    response_model=List[SiteIn],
    status_code=status.HTTP_200_OK,
    description="Get list of all sites",
)
@inject
async def site_data_list(serv: SitesService = Depends(Provide[Services.sites_service])):
    return await serv.get_sites_names()


@router.get(
    "/start_full_check",
    status_code=status.HTTP_200_OK,
    description="Start new full check",
)
@inject
async def start_full_check(
    background_tasks: BackgroundTasks,
    worker: SiteValidator = Depends(Provide[Workers.site_validator_worker]),
):
    background_tasks.add_task(worker.starter)


@router.post(
    "/get_report",
    response_model=ReportOut,
    status_code=status.HTTP_200_OK,
    description="Get report for page by page credits",
)
@inject
async def get_report(
    item: ReportIn,
    serv: ReportsService = Depends(Provide[Services.reports_service]),
):
    return await serv.get_report(item)


@router.post(
    "/update_site",
    response_model=SiteIn,
    status_code=status.HTTP_202_ACCEPTED,
    description="Site status update",
)
@inject
async def update_site(
    item: SiteIn,
    serv: SitesService = Depends(Provide[Services.sites_service]),
):
    return await serv.update_site(item)


@router.get(
    "/get_all_reports",
    response_model=List[ReportOut],
    status_code=status.HTTP_200_OK,
    description="Get all reports from all sites",
)
@inject
async def get_reports(
    serv: ReportsService = Depends(Provide[Services.reports_service]),
):
    return await serv.get_all_reports()
