"""Base business models.

All models *must* be inherited by them.
"""

from .api_exception import BaseException
from .enum import BaseEnum
from .model import BaseModel, Model
