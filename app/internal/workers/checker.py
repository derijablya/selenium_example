import datetime
import time

import aiohttp
import selenium.webdriver.support.expected_conditions as EC
from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from seleniumwire import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support.ui import WebDriverWait
from app.internal import services
from app.internal.workers import generator
from app.pkg import models
from app.pkg.logger import get_logger
from app.pkg.settings import settings


class BasePage:
    def __init__(
        self,
        site_data,
        reports_service: services.ReportsService,
        vectors_service: services.VectorService,
        city_service: services.CityService,
        sites_service: services.SitesService,
    ):
        # proxy_current = generator.GeneratorService().generate_proxy()
        # opts = Options()
        chrome_options = webdriver.ChromeOptions()
        # Option for proxy
        # opts.add_argument("--proxy-server=socks5://%s}" % proxy_current)


        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument("--profile-directory=Default")
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--disable-plugins-discovery")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--verbose")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")

        # opts.add_argument('--allow_remote')
        # wire_options = {
        #     'proxy': {
        #         'http': f'http://{proxy_current}',
        #         'https': f'https://{proxy_current}',
        #         'no_proxy': 'localhost,127.0.0.1',
        #     }
        # }
        self.driver = webdriver.Remote(
            command_executor=f"http://{settings.SELENIUM_HOST}:4444",
            options=chrome_options,
        )

        self.wait = WebDriverWait(self.driver, 10)
        self.actions = ActionChains(self.driver)
        self.__logger = get_logger(__name__)
        self.site_data = site_data

        offset = datetime.timedelta(hours=3)
        self.tz = datetime.timezone(offset, name="MSK")
        self.res_services = []
        self.res_min_valid = False
        self.res_min_value: float = 0
        self.res_max_valid = False
        self.res_max_value: float = 0
        self.res_course_in_valid = False
        self.res_course_out_valid = False
        self.res_course_in_value: float = 0
        self.res_course_out_value: float = 0
        self.res_fatal = False
        self.texts_valid = False
        self.current_result_model: dict = {
            "url": self.site_data.url,
            "from_code": self.site_data.from_code,
            "to_code": self.site_data.to_code,
            "city_code": self.site_data.city_code,
            "lang": self.site_data.lang,
            "min_value_selenium": self.res_min_value,
            "min_value_db": float(self.site_data.minamount_v.split()[0]),
            "min_valid": self.res_min_valid,
            "max_value_selenium": self.res_max_value,
            "max_value_db": float(self.site_data.maxamount_v.split()[0]),
            "max_valid": self.res_max_valid,
            "in_value_selenium": self.res_course_in_value,
            "in_value_db": self.site_data.in_v,
            "in_valid": self.res_course_in_valid,
            "out_value_selenium": self.res_course_out_value,
            "out_value_db": self.site_data.out_v,
            "out_valid": self.res_course_out_valid,
            "texts": self.texts_valid,
            "services": self.res_services,
            "date_time": datetime.datetime.now(tz=self.tz),
            "fatal": self.res_fatal,
            "site_url": self.site_data.site_url.split("//")[1],
        }
        self.reports_service = reports_service
        self.vectors_service = vectors_service
        self.city_service = city_service
        self.sites_service = sites_service

    def process_action(self):
        def dec(func):
            def inner(*args, **kwargs):
                try:

                    func(*args, **kwargs)
                except Exception:
                    self.__logger.exception(
                        f"Sudden error in {func.__name__} on {self.site_data.url}",
                    )
                    self.close()
                    self.res_fatal = True
                    self.current_result_model["services"] = self.res_services
                    self.texts_valid = False
                    self.current_result_model["texts"] = self.texts_valid
                    self.current_result_model["fatal"] = self.res_fatal
                    self.current_result_model["date_time"] = datetime.datetime.now(
                        tz=self.tz,
                    )

                    raise Exception(
                        f"Sudden error for site {self.site_data.url} in {func.__name__}",
                    )

            return inner

        return dec

    def open(self):
        self.driver.get(self.site_data.url)

    def close(self):
        self.driver.quit()

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def input_and_submit(self, locator, value):
        find_field = self.wait.until(EC.presence_of_element_located(locator))
        find_field.click()
        find_field.clear()
        find_field.send_keys(value)
        find_field.send_keys(Keys.ENTER)

    def is_present(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def check_error_input(self, locator, locator_error):
        find_field = self.wait.until(EC.presence_of_element_located(locator))
        find_field.click()
        find_field.clear()
        find_field.click()
        find_field.send_keys("0")
        find_field.send_keys(Keys.ENTER)
        time.sleep(1)
        self.is_present(locator_error)
        find_field.click()
        find_field.clear()

    def change_proxy(self):
        self.driver.quit()
        myproxy = generator.GeneratorService().generate_proxy()
        opts = webdriver.ChromeOptions()
        opts.add_argument("--proxy-server=%s" % myproxy)
        self.driver = webdriver.Remote(
            command_executor=f"http://{settings.SELENIUM_HOST}:4444",
            options=opts,
        )
        self.wait = WebDriverWait(self.driver, 7)
        self.actions = ActionChains(self.driver)

    def input_field(self, locator, value):
        find_field = self.wait.until(EC.presence_of_element_located(locator))
        find_field.click()
        find_field.clear()
        find_field.send_keys(value)

    def get_whole_page(self):
        return self.driver.page_source

    def get_page_title(self):
        return self.driver.title

    def final_page(self):
        self.close()
        self.__logger.info(
            f"""
                --------------------
                Site validated: {self.site_data.url}
                Min: {self.res_min_valid}
                Max: {self.res_max_valid}
                Course IN: {self.res_course_in_valid}
                Course OUT: {self.res_course_out_valid}
                Services: {self.res_services}
                Texts: {self.texts_valid}
                Fatal: {self.res_fatal}
                --------------------
                """,
        )
        self.current_result_model["fatal"] = self.res_fatal
        self.current_result_model["texts"] = self.texts_valid
        self.current_result_model["date_time"] = datetime.datetime.now(tz=self.tz)
        return models.SeleniumOutReport(**self.current_result_model)

    @staticmethod
    async def check_status_selenium():
        async with aiohttp.ClientSession() as session:
            async with session.get("http://selenoid:4444/wd/hub/status") as resp:
                res = await resp.json()
                return res["value"]["ready"]
