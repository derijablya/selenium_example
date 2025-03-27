import pytest

from app.pkg.settings import settings as _settings


@pytest.fixture()
async def settings():
    if _settings.POSTGRES_DB.startswith("test_"):
        return _settings

    _settings.POSTGRES_DB = f"test_{_settings.POSTGRES_DB}"
    return _settings
