import xmltodict

from app.pkg import models
from app.pkg.settings import settings
import aiohttp

__all__ = ["XMLParseService"]


class XMLParseService:
    @staticmethod
    async def parse_xml() -> list[models.XMLParsedVector]:
        if settings.XML_URL:
            async with aiohttp.ClientSession() as session:
                async with session.get(settings.XML_URL) as resp:
                    doc = await resp.text()
                    doc = xmltodict.parse(doc)
                    res: list[models.XMLParsedVector] = []
                    for item in doc["rates"]["item"]:
                        res.append(models.XMLParsedVector(**item))
                    return res
        else:
            with open("app/internal/services/cleanbtc.xml") as fd:
                doc = xmltodict.parse(fd.read())

            res: list[models.XMLParsedVector] = []
            for item in doc["rates"]["item"]:
                res.append(models.XMLParsedVector(**item))
            return res
