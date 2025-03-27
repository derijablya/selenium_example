from typing import List

from app.internal.repository.postgresql.connection import get_connection
from app.internal.repository.postgresql.handlers.collect_response import (
    collect_response,
)
from app.internal.repository.repository import Repository
from app.pkg import models

__all__ = ["ReportsRepository"]


class ReportsRepository(Repository):
    @collect_response
    async def add_report(self, cmd: str) -> models.SeleniumOutReport:
        q = f"""
        insert into reports 
            (url,
            from_code,
            to_code,
            city_code,
            lang,
            min_value_selenium,
            min_value_db,
            min_valid,
            max_value_selenium,
            max_value_db,
            max_valid,
            in_value_selenium,
            in_value_db,
            in_valid,
            out_value_selenium,
            out_value_db,
            out_valid,
            texts,
            services,
            date_time,
            fatal,
            site_url)
        values {cmd}
        on conflict (url, from_code, to_code, city_code, lang)
        do update set
            min_value_selenium = EXCLUDED.min_value_selenium,
            min_value_db = EXCLUDED.min_value_db,
            min_valid = EXCLUDED.min_valid,
            max_value_selenium = EXCLUDED.max_value_selenium,
            max_value_db = EXCLUDED.max_value_db,
            max_valid = EXCLUDED.max_valid,
            in_value_selenium = EXCLUDED.in_value_selenium,
            in_value_db = EXCLUDED.in_value_db,
            in_valid = EXCLUDED.in_valid,
            out_value_selenium = EXCLUDED.out_value_selenium,
            out_value_db = EXCLUDED.out_value_db,
            out_valid = EXCLUDED.out_valid,
            texts = EXCLUDED.texts,
            services = EXCLUDED.services,
            date_time = EXCLUDED.date_time,
            fatal = EXCLUDED.fatal,
            site_url = EXCLUDED.site_url
        returning
            url,
            from_code,
            to_code,
            city_code,
            lang,
            min_value_selenium,
            min_value_db,
            min_valid,
            max_value_selenium,
            max_value_db,
            max_valid,
            in_value_selenium,
            in_value_db,
            in_valid,
            out_value_selenium,
            out_value_db,
            out_valid,
            texts,
            services,
            date_time,
            fatal,
            site_url;
        """
        async with get_connection() as cur:
            await cur.execute(q)
            return await cur.fetchone()


    @collect_response
    async def get_report(self, cmd: models.ReportIn) -> models.SeleniumOutReport:
        q = """
            select
                url,
                from_code,
                to_code,
                city_code,
                lang,
                min_value_selenium,
                min_value_db,
                min_valid,
                max_value_selenium,
                max_value_db,
                max_valid,
                in_value_selenium,
                in_value_db,
                in_valid,
                out_value_selenium,
                out_value_db,
                out_valid,
                texts,
                services,
                date_time,
                fatal,
                site_url
            from reports
            where site_url = %(site_url)s
                and city_code = %(city_code)s
                and from_code = %(from_code)s
                and to_code = %(to_code)s
                and lang = %(lang)s;
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()

    @collect_response
    async def get_reports(self) -> List[models.SeleniumOutReport]:
        q = f"""
                select
                    url,
                    from_code,
                    to_code,
                    city_code,
                    lang,
                    min_value_selenium,
                    min_value_db,
                    min_valid,
                    max_value_selenium,
                    max_value_db,
                    max_valid,
                    in_value_selenium,
                    in_value_db,
                    in_valid,
                    out_value_selenium,
                    out_value_db,
                    out_valid,
                    texts,
                    services,
                    date_time,
                    fatal,
                    site_url
                from reports;
            """
        async with get_connection() as cur:
            await cur.execute(q)
            return await cur.fetchall()
