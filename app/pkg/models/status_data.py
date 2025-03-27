from app.pkg.models.base import BaseModel

__all__ = ["StatusModel"]


class BaseStatus(BaseModel):
    """Base model for status."""


class StatusModel(BaseStatus):
    status: str
