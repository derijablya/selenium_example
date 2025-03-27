import asyncio

from celery import Celery

from app.configuration import __containers__
from app.internal.workers.site_validator import start_new_check_request
from app.pkg import connectors
from app.pkg.models import CeleryConfig

celery = Celery(__name__)
celery.conf.broker_url = CeleryConfig.REDIS_URL.value
celery.conf.result_backend = CeleryConfig.REDIS_URL.value
celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Europe/Moscow",
    enable_utc=True,
)


@celery.task(name="start_check")
def start_check():
    __containers__.set_environment(
        connector_class=connectors.Connectors,
        pkg_name=__name__,
    )
    __containers__.wire_packages()
    asyncio.run(start_new_check_request())


celery.conf.beat_schedule = CeleryConfig.SCHEDULE_CONFIG.value

celery.autodiscover_tasks()
