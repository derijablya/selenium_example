"""
create cities table
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
        """
    create table cities (
        city_id integer not null,
        city_name varchar(30) not null,
        city_lang varchar(10) not null,
        city_code varchar(10) not null,
        city_code_name varchar(30) not null,
        city_is_main bool not null,
        primary key (city_id, city_lang, city_code)
    );
         """
    )
]
