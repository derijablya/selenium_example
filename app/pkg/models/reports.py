from datetime import datetime
from typing import List

from app.pkg.models.base import BaseModel

__all__ = [
    "SeleniumOutReport",
    "NumberDataOutReport",
    "InfoOutReport",
    "LanguageOutReport",
    "CityOutReport",
    "VectorOutReport",
    "ReportOut",
    "ReportIn",
    "SeleniumOutReportWithoutDate",
]


class BaseReportModel(BaseModel):
    """Base model for report."""


class SeleniumOutReport(BaseReportModel):
    url: str
    from_code: str
    to_code: str
    city_code: str
    lang: str

    min_value_selenium: float
    min_value_db: float
    min_valid: bool

    max_value_selenium: float
    max_value_db: float
    max_valid: bool

    in_value_selenium: float
    in_value_db: float
    in_valid: bool

    out_value_selenium: float
    out_value_db: float
    out_valid: bool

    texts: bool
    services: list
    date_time: datetime
    fatal: bool
    site_url: str


class SeleniumOutReportWithoutDate(BaseReportModel):
    url: str
    from_code: str
    to_code: str
    city_code: str
    lang: str

    min_value_selenium: float
    min_value_db: float
    min_valid: bool

    max_value_selenium: float
    max_value_db: float
    max_valid: bool

    in_value_selenium: float
    in_value_db: float
    in_valid: bool

    out_value_selenium: float
    out_value_db: float
    out_valid: bool

    texts: bool
    services: list
    fatal: bool
    site_url: str


class NumberDataOutReport(BaseReportModel):
    fact_value: float
    expected_value: float
    valid: bool


class InfoOutReport(BaseReportModel):
    current_page_url: str
    min_info: NumberDataOutReport
    max_info: NumberDataOutReport
    in_info: NumberDataOutReport
    out_info: NumberDataOutReport
    texts: bool
    services: list
    last_time_checked: datetime
    fatal: bool


class LanguageOutReport(BaseReportModel):
    lang: str
    info: InfoOutReport


class CityOutReport(BaseReportModel):
    city_code: str
    langs: List[LanguageOutReport]


class VectorOutReport(BaseReportModel):
    from_code: str
    to_code: str
    cities: List[CityOutReport]


class ReportOut(BaseReportModel):
    site_url: str
    vectors: List[VectorOutReport]


class ReportIn(BaseReportModel):
    site_url: str
    from_code: str
    to_code: str
    city_code: str
    lang: str
