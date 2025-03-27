import time

from selenium.webdriver.common.by import By

from app.internal.workers import generator
from app.internal.workers.checker import BasePage


class Example1(BasePage):
    # Page 1
    PAGE1_TEXT = (By.CLASS_NAME, "notice_message_text_ins")
    PAGE1_MINMAX = (By.CLASS_NAME, "span_give_max")
    PAGE1_COURSE = (By.CLASS_NAME, "xchange_info_line")
    PAGE1_CALCULATOR_INPUT = (By.NAME, "sum1")
    PAGE1_CALCULATOR_ERROR = (
        By.XPATH,
        '//*[@id="exch_html"]/div[2]/div/div[1]/div[1]/div[2]/div/div[5]/div/div[2]/div',
    )
    # Contact fields
    PAGE1_CONTACT_EMAIL = (By.ID, "cf6")
    PAGE1_CONTACT_TEL = (By.ID, "cf4")
    PAGE1_CONTACT_TG = (By.ID, "cf8")
    # PAGE1_CONTACT_AGREE = (By.NAME, "check_rule")
    # PAGE1_CONTACT_AGREE = (By.XPATH, '// *[ @ id = "exch_html"] / div[2] / div / div[5] / div')
    PAGE1_CONTACT_AGREE = (By.XPATH, '//*[@id="exch_html"]/div[2]/div/div[5]')
    PAGE1_CONTACT_SUBMIT = (By.CLASS_NAME, "xchange_submit")
    # Page 2
    PAGE2_TEXT = (By.CLASS_NAME, "block_instruction_ins")
    PAGE2_PAYMENT = (By.CLASS_NAME, "block_payinfo")
    PAGE2_PAID = (By.CLASS_NAME, "cancel_paybutton")
    # Page 3
    PAGE3_TEXT = (By.CLASS_NAME, "block_payinfo_ins")

    # @BasePage.process_action
    def page1_get_text(self):
        page1_text = self.is_present(self.PAGE1_TEXT).text
        page1_text_from_db = self.site_data.text_v
        if page1_text != page1_text_from_db:
            pass
        else:
            self.texts_valid = True
            self.current_result_model["texts"] = self.texts_valid

    # @BasePage.process_action
    def page1_get_minmax(self):
        page1_minmax = self.is_present(self.PAGE1_MINMAX).text.split()
        page1_min, page1_max = page1_minmax[1], page1_minmax[-2]
        self.res_min_value, self.res_max_value = float(page1_min), float(page1_max)
        page1_min_from_db = self.site_data.minamount_v.split()[0]
        page1_max_from_db = self.site_data.maxamount_v.split()[0]
        if page1_min != page1_min_from_db:
            pass
        else:
            self.res_min_valid = True

        if page1_max != page1_max_from_db:
            pass
        else:
            self.res_max_valid = True
        self.current_result_model["min_value_selenium"] = self.res_min_value
        self.current_result_model["min_value_valid"] = self.res_min_valid
        self.current_result_model["max_value_selenium"] = self.res_max_value
        self.current_result_model["max_value_valid"] = self.res_max_valid

    # @BasePage.process_action
    def page1_get_course(self):
        page1_course = self.is_present(self.PAGE1_COURSE).text.split()
        page1_course_from, page1_course_to = page1_course[2], page1_course[-2]
        self.res_course_in_value, self.res_course_out_value = float(
            page1_course_from,
        ), float(page1_course_to)
        page1_course_in_from_db = str(self.site_data.in_v)
        page1_course_out_from_db = str(self.site_data.out_v)
        if page1_course_in_from_db != page1_course_from:
            pass
        else:
            self.res_course_in_valid = True
        if page1_course_out_from_db != page1_course_to:
            pass
        else:
            self.res_course_out_valid = True
        self.current_result_model["in_value_selenium"] = self.res_course_in_value
        self.current_result_model["in_value_valid"] = self.res_course_in_valid
        self.current_result_model["out_value_selenium"] = self.res_course_out_value
        self.current_result_model["out_value_valid"] = self.res_course_out_valid

    def page1_check_calculator(self):
        try:
            self.check_error_input(
                self.PAGE1_CALCULATOR_INPUT,
                self.PAGE1_CALCULATOR_ERROR,
            )
        except Exception:
            self.res_services.append("Калькулятор не работает")
            self.current_result_model["services"] = self.res_services

    # @BasePage.process_action
    def page1_input_calculator(self):
        page1_minmax = self.is_present(self.PAGE1_MINMAX).text.split()
        page1_min, page1_max = float(page1_minmax[1]), float(page1_minmax[-2])
        page_average = (page1_min + page1_max) / 2
        self.input_field(self.PAGE1_CALCULATOR_INPUT, str(page_average))

    # @BasePage.process_action
    def page1_input_email(self):
        email = generator.GeneratorService().generate_email()
        self.input_field(self.PAGE1_CONTACT_EMAIL, email)

    # @BasePage.process_action
    def page1_input_tel(self):
        tel = generator.GeneratorService().generate_tel()
        self.input_field(self.PAGE1_CONTACT_TEL, tel)

    # @BasePage.process_action
    def page1_input_tg(self):
        tg = generator.GeneratorService().generate_tg()
        self.input_field(self.PAGE1_CONTACT_TG, tg)

    # @BasePage.process_action
    def page1_agree(self):
        self.click(self.PAGE1_CONTACT_AGREE)

    # @BasePage.process_action
    def page1_submit(self):
        self.click(self.PAGE1_CONTACT_SUBMIT)

    # @BasePage.process_action
    def page2_get_text(self):
        page2_text = self.is_present(self.PAGE2_TEXT).text
        page2_text_from_db = self.site_data.text_v
        if page2_text != page2_text_from_db:
            self.texts_valid = False
        else:
            pass

    # @BasePage.process_action
    def page2_get_payment(self):
        page2_payment = self.is_present(self.PAGE2_PAYMENT).text
        if (
            self.site_data.from_name in page2_payment
            and self.site_data.to_name in page2_payment
        ):
            pass
        else:

            self.texts_valid = False

    # @BasePage.process_action
    def page2_paid(self):
        self.click(self.PAGE2_PAID)

    # @BasePage.process_action
    def page3_get_text(self):
        page3_text = self.is_present(self.PAGE3_TEXT).text
        if (
            self.site_data.from_name in page3_text
            and self.site_data.to_name in page3_text
        ):
            pass
        else:
            self.texts_valid = False

    def run_check(self):
        try:
            self.open()
            self.page1_agree()
            self.page1_get_text()
            self.page1_get_minmax()
            self.page1_get_course()
            self.page1_check_calculator()
            self.page1_input_calculator()
            self.page1_input_email()
            self.page1_input_tel()
            self.page1_input_tg()
            self.page1_submit()
            self.page2_get_text()
            self.page2_get_payment()
            self.page2_paid()
            self.page3_get_text()
            return self.final_page()
        except Exception:
            raise Exception

