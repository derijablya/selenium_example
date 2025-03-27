from app.pkg.models.base import BaseModel

__all__ = ["Vector", "VectorIn", "VectorOut", "VectorTextIn", "VectorNamesTextOut"]


class BaseVectorModel(BaseModel):
    """Base model for vector."""


class Vector(BaseVectorModel):
    site_url: str
    from_code: str
    from_name: str
    to_code: str
    to_name: str
    is_crypto_first: bool
    city_is_main: bool
    lang: str
    text_v: str


class VectorIn(BaseVectorModel):
    site_url: str
    lang: str
    city_is_main: bool


class VectorOut(BaseVectorModel):
    from_code: str
    from_name: str
    to_code: str
    to_name: str
    text_v: str


class VectorTextIn(BaseVectorModel):
    site_url: str
    lang: str
    city_is_main: bool
    from_v: str
    to_v: str


class VectorNamesTextOut(BaseVectorModel):
    from_name: str
    to_name: str
    text_v: str
