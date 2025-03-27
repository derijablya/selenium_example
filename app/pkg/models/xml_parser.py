from pydantic import Field

from app.pkg.models.base import BaseModel

__all__ = ["XMLParsedVector"]


class BaseXMLVectorModel(BaseModel):
    """Base model for XMLParser."""


class XMLParsedVector(BaseXMLVectorModel):
    from_v: str = Field(alias="from")
    to_v: str = Field(alias="to")
    in_v: float = Field(alias="in")
    out_v: float = Field(alias="out")
    amount_v: float = Field(alias="amount")
    minamount_v: str = Field(alias="minamount")
    maxamount_v: str = Field(alias="maxamount")
    param_v: str = Field(alias="param")
    city_code: str = Field(alias="city")
