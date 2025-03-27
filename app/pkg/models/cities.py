from app.pkg.models.base import BaseModel

__all__ = [
    "City",
    "CityNameLangIsMain",
]


class BaseCity(BaseModel):
    """Base model for city."""


class City(BaseCity):
    city_id: int
    city_name: str
    city_lang: str
    city_code: str
    city_code_name: str
    city_is_main: bool


class CityNameLangIsMain(BaseCity):
    city_name: str
    city_lang: str
    city_code_name: str
    city_is_main: bool
