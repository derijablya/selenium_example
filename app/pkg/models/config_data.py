from app.pkg.models.base import BaseEnum
from app.pkg.settings import settings

all = ["CeleryConfig", "GeneratorConfig"]


class CeleryConfig(BaseEnum):
    pass


class GeneratorConfig(BaseEnum):
    LIST_OF_TG = ["14f80be7-b620-4bba-bdfb-73a0109b575c"]
    LIST_OF_EMAIL_HOSTS = [
        "6d3d70911203fbb35a2664a768e936.ru",
    ]
    LIST_OF_EMAIL_USERNAMES = ["14f80be7-b620-4bba-bdfb-73a0109b575c"]
    LIST_OF_PROXIES = [
        ""
    ]
