import datetime

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, BackgroundTasks, Depends
from starlette import status

from app.internal.services import (
    CityService,
    ReportsService,
    Services,
    SitesService,
    VectorService,
)
from app.pkg.models import (
    City,
    SeleniumOutReport,
    SeleniumOutReportWithoutDate,
    SiteIn,
    Vector,
)

__all__ = ["router"]

router = APIRouter(tags=["Add info"])


@router.post(
    "/add_city_data",
    response_model=City,
    status_code=status.HTTP_201_CREATED,
    description="Add city data",
)
@inject
async def add_city_data(
    item: City,
    serv: CityService = Depends(Provide[Services.city_service]),
):
    return await serv.add_city_data(item)


@router.post(
    "/add_vector_data",
    response_model=Vector,
    status_code=status.HTTP_201_CREATED,
    description="Add vector data",
)
@inject
async def add_vector_data(
    item: Vector,
    serv: VectorService = Depends(Provide[Services.vector_service]),
):
    return await serv.add_vector_data(item)


@router.post(
    "/add_site_data",
    response_model=SiteIn,
    status_code=status.HTTP_201_CREATED,
    description="Add site data",
)
@inject
async def add_site_data(
    item: SiteIn,
    serv: SitesService = Depends(Provide[Services.sites_service]),
):
    return await serv.add_site(item)


@router.post(
    "/add_report_data",
    status_code=status.HTTP_201_CREATED,
    description="Add report data",
)
@inject
async def add_report_data(
    item: SeleniumOutReportWithoutDate,
    background_tasks: BackgroundTasks,
    serv: ReportsService = Depends(Provide[Services.reports_service]),
):
    data_raw = item.dict()
    offset = datetime.timedelta(hours=3)
    tz = datetime.timezone(offset, name="MSK")
    data_raw["date_time"] = datetime.datetime.now(tz=tz)
    background_tasks.add_task(serv.upsert_report, SeleniumOutReport(**data_raw))
