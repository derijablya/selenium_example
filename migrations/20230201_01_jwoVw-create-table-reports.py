"""
create table reports
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
        """
        create table reports (
	        url varchar(100) not null,
            from_code varchar(15) not null,
            to_code varchar(15) not null,
            city_code varchar(10) not null,
            lang varchar(10) not null,
            min_value_selenium decimal not null,
            min_value_db decimal not null,
            min_valid bool not null,
            max_value_selenium decimal not null,
            max_value_db decimal not null,
            max_valid bool not null,
            in_value_selenium decimal not null,
            in_value_db decimal not null,
            in_valid bool not null,
            out_value_selenium decimal not null,
            out_value_db decimal not null,
            out_valid bool not null,
            texts bool not null,
            services varchar[] not null default array[]::varchar[],
            date_time timestamp not null,
            fatal bool not null,
            site_url varchar(100) not null,
            primary key (url, from_code, to_code, city_code, lang));"""
    )
]
