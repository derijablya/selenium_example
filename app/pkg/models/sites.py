from app.pkg.models.base import BaseModel

__all__ = [
    "SiteIn",
    "SiteOut",
    "SiteUpdate",
    "SiteNameOnly",
    "SiteFull",
]


class BaseSiteModel(BaseModel):
    """Base model for site."""


class SiteIn(BaseSiteModel):
    site_name: str
    site_status: bool


class SiteFull(BaseSiteModel):
    site_name: str
    site_url: str
    site_status: bool


class SiteOut(BaseSiteModel):
    site_url: str
    site_status: bool


class SiteUpdate(BaseSiteModel):
    site_name: str
    site_status: bool


class SiteNameOnly(BaseSiteModel):
    site_name: str
