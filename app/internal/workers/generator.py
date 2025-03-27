import random

from app.pkg.logger import get_logger
from app.pkg.models import GeneratorConfig


class GeneratorService:
    def __init__(self):
        self.__logger = get_logger(__name__)

    @staticmethod
    def generate_proxy():
        list_of_proxies = GeneratorConfig.LIST_OF_PROXIES.value
        return random.choice(list_of_proxies)

    @staticmethod
    def generate_email():
        list_of_usernames = GeneratorConfig.LIST_OF_EMAIL_USERNAMES.value
        list_of_domains = GeneratorConfig.LIST_OF_EMAIL_HOSTS.value
        return f"{random.choice(list_of_usernames)}@{random.choice(list_of_domains)}"

    @staticmethod
    def generate_tel():
        return f"999{random.randint(1000000, 9999999)}"

    @staticmethod
    def generate_tg():
        list_of_tg = GeneratorConfig.LIST_OF_TG.value
        return f"{random.choice(list_of_tg)}"
