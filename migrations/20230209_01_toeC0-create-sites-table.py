"""
create sites table
"""

from yoyo import step

__depends__ = {}

steps = [
    step("""
    create table sites
(
    site_url varchar(50) not null,
    site_name varchar(50) not null,
    site_status bool not null default true,
    primary key (site_url)
);
         """)
]
