from typing import List

from app.internal.repository.postgresql.connection import get_connection
from app.internal.repository.postgresql.handlers.collect_response import (
    collect_response,
)
from app.internal.repository.repository import Repository
from app.pkg import models

__all__ = ["SitesRepository"]


class SitesRepository(Repository):
    @collect_response
    async def get_list_of_sites(self) -> List[models.SiteOut]:
        q = """
            select 
            site_url,
            site_status 
            from sites;
            """
        async with get_connection() as cur:
            await cur.execute(q)
            return await cur.fetchall()

    @collect_response
    async def get_list_of_sites_names(self) -> List[models.SiteIn]:
        q = """
                select 
                site_name,
                site_status 
                from sites
                order by site_name;
                """
        async with get_connection() as cur:
            await cur.execute(q)
            return await cur.fetchall()

    @collect_response
    async def add_site(self, cmd: models.SiteIn) -> models.SiteIn:
        site_url = f"https://{cmd.site_name}"
        site_dict = cmd.dict()

        site_dict["site_url"] = site_url
        q = """
            insert into sites (site_name, site_url, site_status)
            values (%(site_name)s, %(site_url)s, %(site_status)s)
            on conflict (site_url)
                do update set site_name=excluded.site_name,
                              site_url=excluded.site_url,
                              site_status=excluded.site_status
            returning site_name, site_status;
            """
        async with get_connection() as cur:
            await cur.execute(q, site_dict)
            return await cur.fetchone()

    @collect_response
    async def change_site_status(self, cmd: models.SiteIn) -> models.SiteIn:
        q = """
            update sites
            set site_status = %(site_status)s
            where site_name = %(site_name)s
            returning site_name, site_status;
            """
        async with get_connection() as cur:
            await cur.execute(q, cmd.dict())
            return await cur.fetchone()
