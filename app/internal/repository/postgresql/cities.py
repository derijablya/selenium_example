from typing import List

from app.internal.repository.postgresql.connection import get_connection
from app.internal.repository.postgresql.handlers.collect_response import (
    collect_response,
)
from app.internal.repository.repository import Repository
from app.pkg import models

__all__ = ["CitiesRepository"]


class CitiesRepository(Repository):
    @collect_response
    async def get_cities_all(self) -> List[models.City]:
        q = """
        select 
            city_id,
            city_name, 
            city_lang, 
            city_code,
            city_code_name,
            city_is_main 
        from cities;
        """
        async with get_connection() as cur:
            await cur.execute(q)
            return await cur.fetchall()

    @collect_response
    async def get_city_by_code_db(self, code: str) -> List[models.CityNameLangIsMain]:
        q = f"""
        select 
            city_name, 
            city_lang,
            city_code_name,
            city_is_main 
        from cities
        where city_code = '{code}';
        """
        async with get_connection() as cur:
            await cur.execute(q)
            return await cur.fetchall()

    @collect_response
    async def add_city(self, data: models.City) -> models.City:
        q = """
            INSERT INTO 
                cities (city_id, city_name, city_lang, city_code, city_code_name, city_is_main)
                values 
                    (%(city_id)s, 
                    %(city_name)s, 
                    %(city_lang)s, 
                    %(city_code)s, 
                    %(city_code_name)s, 
                    %(city_is_main)s)
            on conflict (city_id, city_lang, city_code)
            do update set
                city_id = EXCLUDED.city_id,
                city_name = EXCLUDED.city_name, 
                city_lang = EXCLUDED.city_lang, 
                city_code = EXCLUDED.city_code, 
                city_code_name = EXCLUDED.city_code_name, 
                city_is_main = EXCLUDED.city_is_main
            returning 
                city_id, 
                city_name, 
                city_lang, 
                city_code, 
                city_code_name, 
                city_is_main;
            """
        async with get_connection() as cur:
            await cur.execute(q, data.to_dict())
            return await cur.fetchone()
