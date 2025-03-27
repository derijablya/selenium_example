from typing import List

from app.internal.repository.postgresql.connection import get_connection
from app.internal.repository.postgresql.handlers.collect_response import (
    collect_response,
)
from app.internal.repository.repository import Repository
from app.pkg import models

__all__ = ["VectorsRepository"]


class VectorsRepository(Repository):
    @collect_response
    async def get_vectors_by_city_url_lang(
        self,
        cmd: models.VectorIn,
    ) -> List[models.VectorOut]:
        q = """
        select
            from_code,
            from_name,
            to_code,
            to_name,
            text_v
        from vectors
        where city_is_main = %(city_is_main)s
            and site_url = %(site_url)s
            and lang = %(lang)s; 
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchall()

    @collect_response
    async def get_vector_text(
        self,
        cmd: models.VectorTextIn,
    ) -> models.VectorNamesTextOut:
        q = """
            select
                from_name,
                to_name,
                text_v
            from vectors
            where 
                city_is_main = %(city_is_main)s
                and site_url = %(site_url)s
                and lang = %(lang)s
                and from_code = %(from_v)s
                and to_code = %(to_v)s;
            """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()

    @collect_response
    async def add_vector(self, cmd: models.Vector) -> models.Vector:
        q = """
            insert into vectors
                (site_url, from_code, from_name, to_code, to_name, city_is_main, lang, is_crypto_first, text_v)
                values
                (%(site_url)s, 
                %(from_code)s, 
                %(from_name)s,
                %(to_code)s,
                %(to_name)s, 
                %(city_is_main)s, 
                %(lang)s, 
                %(is_crypto_first)s, 
                %(text_v)s)
            on conflict (site_url, from_code, to_code, city_is_main, lang)
            do update set
                site_url = EXCLUDED.site_url,
                from_code = EXCLUDED.from_code,
                from_name = EXCLUDED.from_name,
                to_code = EXCLUDED.to_code,
                to_name = EXCLUDED.to_name,
                city_is_main = EXCLUDED.city_is_main,
                lang = EXCLUDED.lang,
                is_crypto_first = EXCLUDED.is_crypto_first,
                text_v = EXCLUDED.text_v 
            returning
                site_url,
                from_code,
                from_name,
                to_code,
                to_name,
                city_is_main,
                lang,
                is_crypto_first,
                text_v;
            """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()
