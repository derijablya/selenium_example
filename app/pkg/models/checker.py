from app.pkg.models.base import BaseModel

__all__ = [
    "FormUrlIn",
    "FormUrlOut",
    "LinkFormerData",
]


class BaseCheckerModel(BaseModel):
    """Base model for checker."""


class FormUrlIn(BaseCheckerModel):
    site_url: str
    from_v: str
    to_v: str
    lang: str
    city_code: str


class FormUrlOut(BaseCheckerModel):
    url: str


class LinkFormerData(BaseCheckerModel):
    url: str
    city_name: str
    city_code: str
    city_code_name: str

    from_code: str
    from_name: str
    to_code: str
    to_name: str

    in_v: float
    out_v: float
    amount_v: float
    minamount_v: str
    maxamount_v: str
    text_v: str
    lang: str

    site_url: str
