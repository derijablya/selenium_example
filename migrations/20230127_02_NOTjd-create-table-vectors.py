"""
create table vectors
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
        """
        create table vectors (
            site_url varchar(100) not null,
            from_code varchar(15) not null,
            from_name varchar(50) not null,
            to_code varchar(15) not null,
            to_name varchar(50) not null,
            is_crypto_first bool not null,
            city_is_main bool not null,
            lang varchar(10) not null,
            text_v text not null,
            primary key (site_url, from_code, to_code, city_is_main, lang)
        );
         """
    )
]
